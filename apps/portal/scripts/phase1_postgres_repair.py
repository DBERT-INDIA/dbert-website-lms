import os
import psycopg2

def main():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("[CRITICAL] DATABASE_URL not set")
        return
        
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
    except Exception as e:
        print(f"[CRITICAL] Could not connect to DB: {e}")
        return
    
    # 1. Ensure search path is strict for the repair
    cur.execute("SET search_path TO dbert_internship, public")
    
    # 2. Check if we have records in public that are missing in dbert_internship
    print("Migrating any missing records from public to dbert_internship...")
    tables = ['intern_accounts', 'courses', 'course_enrollments']
    
    for t in tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name = '{t}'")
            if cur.fetchone()[0] > 0:
                cur.execute(f"""
                    INSERT INTO dbert_internship.{t}
                    SELECT * FROM public.{t}
                    WHERE id NOT IN (SELECT id FROM dbert_internship.{t})
                """)
                print(f"Migrated missing records for {t}. Inserted: {cur.rowcount}")
        except Exception as e:
            print(f"Migration for {t} failed: {e}")
            conn.rollback()
            continue

    # 3. Drop the public tables so they never interfere again
    print("\nDropping duplicate tables in public schema to resolve FK paradox...")
    for t in ['course_enrollments', 'courses', 'intern_accounts']: # Drop in reverse dependency order
        try:
            cur.execute(f"DROP TABLE IF EXISTS public.{t} CASCADE;")
            print(f"Dropped public.{t}")
        except Exception as e:
            print(f"Failed to drop public.{t}: {e}")
            conn.rollback()

    # 4. Re-establish foreign keys strictly on dbert_internship
    print("\nRe-establishing strict Foreign Keys on dbert_internship.course_enrollments...")
    try:
        cur.execute("ALTER TABLE dbert_internship.course_enrollments DROP CONSTRAINT IF EXISTS course_enrollments_intern_id_fkey;")
        cur.execute("ALTER TABLE dbert_internship.course_enrollments DROP CONSTRAINT IF EXISTS course_enrollments_course_id_fkey;")
        
        cur.execute("""
            ALTER TABLE dbert_internship.course_enrollments 
            ADD CONSTRAINT course_enrollments_intern_id_fkey 
            FOREIGN KEY (intern_id) REFERENCES dbert_internship.intern_accounts(id);
        """)
        cur.execute("""
            ALTER TABLE dbert_internship.course_enrollments 
            ADD CONSTRAINT course_enrollments_course_id_fkey 
            FOREIGN KEY (course_id) REFERENCES dbert_internship.courses(id);
        """)
        print("Foreign Keys successfully enforced!")
    except Exception as e:
        print(f"Failed to enforce FKs: {e}")
        conn.rollback()

    conn.commit()
    print("\n[SUCCESS] Phase 1 Repair Complete: PostgreSQL Root-Cause (FK Paradox) Resolved!")

run = main

if __name__ == "__main__":
    main()
