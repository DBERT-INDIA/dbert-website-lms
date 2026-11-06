import sqlite3
import json
import os
import subprocess
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REGISTRY_PATH = os.path.join(BASE_DIR, "outputs", "certificates_registry.json")
SQLITE_DB = os.path.join(BASE_DIR, "apps", "portal", "internship.db")
SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
SERVER = "ubuntu@3.26.237.171"

def sync_local_sqlite(registry):
    print("=" * 60)
    print("1. Synchronizing Local SQLite Database (apps/portal/internship.db)...")
    print("=" * 60)
    if not os.path.exists(SQLITE_DB):
        print(f"Warning: {SQLITE_DB} does not exist.")
        return

    conn = sqlite3.connect(SQLITE_DB)
    c = conn.cursor()

    updated_certs = 0
    updated_accounts = 0
    created_notifications = 0

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for cert_id, rec in registry.items():
        email = rec["email"].strip().lower()
        issue_date_str = f"{rec.get('issueDate', '2026-10-01')} 10:00:00"
        verify_url = f"https://dbert.in/verify?certid={cert_id}"

        # 1. Update intern_certificates
        c.execute("""
            UPDATE intern_certificates
            SET issued_at = ?, received_at = ?, url = ?, tier = 'dbert_verified'
            WHERE cert_id = ? OR (email IS NOT NULL AND LOWER(email) = ?)
        """, (issue_date_str, issue_date_str, verify_url, cert_id, email))
        if c.rowcount > 0:
            updated_certs += c.rowcount

        # 2. Update intern_accounts to approved
        c.execute("""
            UPDATE intern_accounts
            SET account_status = 'approved', updated_at = ?
            WHERE LOWER(email) = ? AND (account_status IS NULL OR account_status IN ('awaiting_verification', 'pending_approval'))
        """, (now_str, email))
        if c.rowcount > 0:
            updated_accounts += c.rowcount

        # 3. Insert notification if not exists
        c.execute("SELECT id FROM intern_accounts WHERE LOWER(email) = ?", (email,))
        acct = c.fetchone()
        if acct:
            intern_id = acct[0]
            c.execute("""
                SELECT id FROM notifications 
                WHERE intern_id = ? AND link LIKE ?
            """, (intern_id, f"%{cert_id}%"))
            if not c.fetchone():
                c.execute("""
                    INSERT INTO notifications (intern_id, kind, title, body, link, is_read, created_at)
                    VALUES (?, 'certificate', 'Official Verified Credential Packet Issued',
                            'Congratulations! Your 2-Month Internship Certificate, Academic Evaluation, and Letter of Recommendation are now officially verified and available.',
                            ?, 0, ?)
                """, (intern_id, verify_url, now_str))
                created_notifications += 1

    conn.commit()
    conn.close()

    print(f"SQLite Sync Completed:")
    print(f"  - Updated Certificates: {updated_certs}")
    print(f"  - Approved Intern Accounts: {updated_accounts}")
    print(f"  - Generated Notifications: {created_notifications}")


def sync_ec2_postgres(registry):
    print("\n" + "=" * 60)
    print("2. Synchronizing EC2 Production PostgreSQL (dbert_lms.dbert_internship)...")
    print("=" * 60)

    # Build SQL migration commands
    sql_statements = ["SET search_path TO dbert_internship, public;"]

    for cert_id, rec in registry.items():
        email = rec["email"].strip().lower().replace("'", "''")
        issue_date_str = f"{rec.get('issueDate', '2026-10-01')} 10:00:00"
        verify_url = f"https://dbert.in/verify?certid={cert_id}"
        cid_clean = cert_id.replace("'", "''")

        # 1. Update intern_certificates
        sql_statements.append(f"""
            UPDATE dbert_internship.intern_certificates
            SET issued_at = '{issue_date_str}', received_at = '{issue_date_str}', url = '{verify_url}', tier = 'dbert_verified'
            WHERE cert_id = '{cid_clean}' OR (email IS NOT NULL AND LOWER(email) = '{email}');
        """)

        # 2. Update intern_accounts
        sql_statements.append(f"""
            UPDATE dbert_internship.intern_accounts
            SET account_status = 'approved', updated_at = NOW()
            WHERE LOWER(email) = '{email}' AND (account_status IS NULL OR account_status IN ('awaiting_verification', 'pending_approval'));
        """)

        # 3. Insert notification if not exists
        sql_statements.append(f"""
            DO $$
            DECLARE
                v_intern_id INTEGER;
            BEGIN
                SELECT id INTO v_intern_id FROM dbert_internship.intern_accounts WHERE LOWER(email) = '{email}' LIMIT 1;
                IF v_intern_id IS NOT NULL THEN
                    IF NOT EXISTS (SELECT 1 FROM dbert_internship.notifications WHERE intern_id = v_intern_id AND link LIKE '%{cid_clean}%') THEN
                        INSERT INTO dbert_internship.notifications (intern_id, kind, title, body, link, is_read, created_at)
                        VALUES (
                            v_intern_id,
                            'certificate',
                            'Official Verified Credential Packet Issued',
                            'Congratulations! Your 2-Month Internship Certificate, Academic Evaluation, and Letter of Recommendation are now officially verified and available.',
                            '{verify_url}',
                            0,
                            NOW()
                        );
                    END IF;
                END IF;
            END $$;
        """)

    full_sql = "\n".join(sql_statements)
    remote_script_path = "/tmp/sync_db.sql"

    # Write SQL locally to temporary file
    temp_sql_path = os.path.join(BASE_DIR, "scripts", "temp_sync.sql")
    with open(temp_sql_path, "w", encoding="utf-8") as f:
        f.write(full_sql)

    # SCP SQL file to EC2
    print("Uploading SQL batch script to EC2...")
    res_scp = subprocess.run([
        "scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no",
        temp_sql_path, f"{SERVER}:{remote_script_path}"
    ], capture_output=True, text=True)
    if res_scp.returncode != 0:
        print("Error uploading SQL script:", res_scp.stderr)
        return

    # Execute via psql
    print("Executing batch SQL script in PostgreSQL on EC2...")
    remote_exec = f"sudo -u postgres psql -d dbert_lms -f {remote_script_path} > /tmp/psql_output.log 2>&1 && rm -f {remote_script_path}"
    res_exec = subprocess.run([
        "ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no",
        SERVER, remote_exec
    ], capture_output=True, text=True)
    if res_exec.returncode != 0:
        print("Error executing SQL script on EC2:", res_exec.stderr)
    else:
        print("PostgreSQL migration executed successfully on EC2.")

    # Clean up local temp SQL file
    if os.path.exists(temp_sql_path):
        os.remove(temp_sql_path)

def main():
    if not os.path.exists(REGISTRY_PATH):
        print(f"Error: Registry file not found at {REGISTRY_PATH}")
        return

    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)

    print(f"Loaded {len(registry)} credentials from registry.")
    sync_local_sqlite(registry)
    sync_ec2_postgres(registry)

if __name__ == "__main__":
    main()
