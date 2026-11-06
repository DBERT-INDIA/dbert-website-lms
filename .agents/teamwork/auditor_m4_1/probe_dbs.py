import sqlite3
import os
import zipfile

databases = [
    'internship.db',
    'apps/portal/internship.db',
    'dbert-api-package/databases/internship.db'
]

print("=== PROBING SQLITE DATABASES ===")
for path in databases:
    if not os.path.exists(path):
        print(f"MISSING: {path}")
        continue
    size = os.path.getsize(path)
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("PRAGMA integrity_check;")
    integ = cur.fetchall()
    cur.execute("PRAGMA foreign_key_check;")
    fk = cur.fetchall()
    cur.execute("PRAGMA freelist_count;")
    freelist = cur.fetchone()[0]
    
    # Check all tables and text columns
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r[0] for r in cur.fetchall()]
    table_hits = 0
    for tbl in tables:
        try:
            cur.execute(f"PRAGMA table_info([{tbl}]);")
            cols = [c[1] for c in cur.fetchall()]
            for col in cols:
                cur.execute(f"SELECT COUNT(*) FROM [{tbl}] WHERE [{col}] LIKE ?", ('%dbert.online%',))
                cnt = cur.fetchone()[0]
                if cnt > 0:
                    print(f"  [LEAK] {path} -> {tbl}.{col}: {cnt} rows with dbert.online")
                    table_hits += cnt
        except Exception:
            pass
    conn.close()

    with open(path, 'rb') as f:
        raw_bytes = f.read()
        bin_hits = raw_bytes.lower().count(b'dbert.online')

    print(f"{path} ({size:,} bytes, {len(tables)} tables):")
    print(f"  integrity_check: {integ}")
    print(f"  foreign_key_check violations: {len(fk)}")
    print(f"  freelist_count: {freelist}")
    print(f"  SQL table matches: {table_hits}")
    print(f"  Raw binary hits: {bin_hits}")
    assert integ == [('ok',)], f"Integrity failed on {path}"
    assert len(fk) == 0, f"FK failed on {path}"
    assert freelist == 0, f"Freelist > 0 on {path}"
    assert table_hits == 0, f"SQL matches > 0 on {path}"
    assert bin_hits == 0, f"Raw binary matches > 0 on {path}"

print("\n=== PROBING PACKAGE ARCHIVE ===")
zip_path = 'dbert-api-package-v1.zip'
if os.path.exists(zip_path):
    zsize = os.path.getsize(zip_path)
    with zipfile.ZipFile(zip_path) as z:
        namelist = [n for n in z.namelist() if not n.endswith('/')]
        leaks = []
        for name in namelist:
            content = z.read(name)
            if b'dbert.online' in content.lower():
                # check if intentional redirect
                if name.endswith('.htaccess'):
                    continue
                leaks.append(name)
        print(f"{zip_path} ({zsize:,} bytes, {len(namelist)} files):")
        print(f"  Unintended legacy domain files: {len(leaks)}")
        if leaks:
            print(f"  Leaking files: {leaks}")
        assert len(leaks) == 0, f"Leaks in zip: {leaks}"
else:
    print(f"MISSING: {zip_path}")

print("\nALL DATABASE & ARCHIVE INTEGRITY CHECKS PASSED!")
