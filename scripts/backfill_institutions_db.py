#!/usr/bin/env python3
"""
Idempotent PostgreSQL migration & backfill script for:
  1. `institutions` master table (seeded from data/master_institutions_seed.json)
  2. `institution_id` and `affiliated_university` columns on `intern_accounts` & `applications`
  3. Backfilling existing rows using data/college_backfill_mapping.json
"""
import json
import os
import sys

PORTAL_DIR = "/var/www/dbert-website-lms/apps/portal"
DATA_DIR = "/var/www/dbert-website-lms/data"
if os.path.isdir(PORTAL_DIR):
    os.chdir(PORTAL_DIR)
    sys.path.insert(0, PORTAL_DIR)
else:
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(os.path.join(ROOT, "apps", "portal"))
    sys.path.insert(0, os.path.join(ROOT, "apps", "portal"))
    DATA_DIR = os.path.join(ROOT, "data")

import app

SEED_PATH = os.path.join(DATA_DIR, "master_institutions_seed.json")
MAPPING_PATH = os.path.join(DATA_DIR, "college_backfill_mapping.json")


def main():
    print("Loading seed and mapping...")
    seed = json.load(open(SEED_PATH, encoding="utf-8"))
    mapping = json.load(open(MAPPING_PATH, encoding="utf-8"))

    with app.get_db() as conn:
        raw_conn = conn._conn if hasattr(conn, "_conn") else conn
        cur = raw_conn.cursor()

        # 1. Create institutions table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS institutions (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                aliases TEXT DEFAULT '[]',
                affiliated_university TEXT DEFAULT '',
                city TEXT DEFAULT '',
                state TEXT DEFAULT '',
                aishe_code TEXT DEFAULT '',
                source TEXT DEFAULT 'aishe',
                is_verified BOOLEAN DEFAULT TRUE,
                created_at TEXT DEFAULT ''
            );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_inst_name_lower ON institutions (LOWER(name));")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_inst_city_lower ON institutions (LOWER(city));")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_inst_verified ON institutions (is_verified);")

        # 2. Add columns to intern_accounts & applications
        for tbl in ("intern_accounts", "applications"):
            cur.execute(f"ALTER TABLE {tbl} ADD COLUMN IF NOT EXISTS institution_id INTEGER;")
            cur.execute(f"ALTER TABLE {tbl} ADD COLUMN IF NOT EXISTS affiliated_university TEXT DEFAULT '';")
            cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{tbl}_inst_id ON {tbl} (institution_id);")

        raw_conn.commit()

        # 3. Seed institutions if empty
        cur.execute("SELECT COUNT(*) AS cnt FROM institutions;")
        row_cnt = cur.fetchone()
        existing_cnt = row_cnt["cnt"] if isinstance(row_cnt, dict) else row_cnt[0]
        if existing_cnt == 0:
            print(f"Seeding {len(seed)} institutions into PostgreSQL...")
            from psycopg2.extras import execute_values
            rows_to_insert = [
                (
                    r["name"],
                    json.dumps(r.get("aliases") or [], ensure_ascii=False),
                    r.get("affiliated_university") or "",
                    r.get("city") or "",
                    r.get("state") or "",
                    r.get("aishe_code") or "",
                    r.get("source") or "aishe",
                    bool(r.get("is_verified", True)),
                    app.now_str(),
                )
                for r in seed
            ]
            execute_values(
                cur,
                """INSERT INTO institutions
                   (name, aliases, affiliated_university, city, state, aishe_code, source, is_verified, created_at)
                   VALUES %s""",
                rows_to_insert,
                page_size=2000,
            )
            raw_conn.commit()
            print("Seed complete.")
        else:
            print(f"institutions table already has {existing_cnt} rows; skipping bulk insert.")

        # 4. Build name -> id lookup
        cur.execute("SELECT id, name, affiliated_university, city FROM institutions;")
        inst_by_lower = {}
        for row in cur.fetchall():
            # row may be dict (RealDictCursor) or tuple
            if isinstance(row, dict):
                iid, iname, iaff, icity = row["id"], row["name"], row["affiliated_university"], row["city"]
            else:
                iid, iname, iaff, icity = row[0], row[1], row[2], row[3]
            inst_by_lower[iname.strip().lower()] = (iid, iname, iaff or "", icity or "")

        print(f"Loaded {len(inst_by_lower)} institutions from DB for backfill.")

        # 5. Backfill intern_accounts and applications
        for tbl in ("intern_accounts", "applications"):
            cur.execute(f"SELECT id, college, city FROM {tbl};")
            db_rows = cur.fetchall()
            updates_map = []
            updates_clear = []
            for row in db_rows:
                if isinstance(row, dict):
                    rid, rcol, rcity = row["id"], (row["college"] or "").strip(), (row["city"] or "").strip()
                else:
                    rid, rcol, rcity = row[0], (row[1] or "").strip(), (row[2] or "").strip()
                if not rcol:
                    continue
                m = mapping.get(rcol)
                if not m:
                    continue
                if m["action"] == "CLEAR_JUNK":
                    updates_clear.append((rid,))
                elif m["action"] == "MAP":
                    cname = (m.get("canonical_name") or "").strip()
                    info = inst_by_lower.get(cname.lower())
                    if info:
                        iid, canon_name, aff_univ, inst_city = info
                        final_city = inst_city or m.get("city") or rcity
                        final_aff = aff_univ or m.get("affiliated_university") or ""
                        updates_map.append((iid, canon_name, final_aff, final_city, rid))

            if updates_clear:
                cur.executemany(
                    f"UPDATE {tbl} SET college='', institution_id=NULL, affiliated_university='' WHERE id=%s",
                    updates_clear,
                )
            if updates_map:
                from psycopg2.extras import execute_batch
                execute_batch(
                    cur,
                    f"UPDATE {tbl} SET institution_id=%s, college=%s, affiliated_university=%s, city=COALESCE(NULLIF(%s,''), city) WHERE id=%s",
                    updates_map,
                    page_size=1000,
                )
            raw_conn.commit()
            print(f"Backfilled {tbl}: {len(updates_map)} mapped, {len(updates_clear)} junk cleared.")

        # 6. Post-backfill stats
        cur.execute("SELECT COUNT(*) FROM institutions;")
        inst_cnt = cur.fetchone()
        print("Post-backfill institutions count:", inst_cnt[0] if not isinstance(inst_cnt, dict) else inst_cnt["count"])
        for tbl in ("intern_accounts", "applications"):
            cur.execute(f"SELECT COUNT(DISTINCT college) AS uniq_c, COUNT(institution_id) AS linked FROM {tbl} WHERE college IS NOT NULL AND college <> '';")
            st = cur.fetchone()
            print(f"Post-backfill {tbl}:", dict(st) if hasattr(st, "keys") else st)


if __name__ == "__main__":
    main()
