import sqlite3
import csv

def main():
    with open('data/aug_oct_unmatched_pending.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        pending = list(reader)

    emails = [p['email'].strip().lower() for p in pending if p.get('email')]
    print(f"Checking {len(emails)} pending Aug-Oct emails in apps/portal/internship.db...")

    conn = sqlite3.connect('apps/portal/internship.db')
    c = conn.cursor()

    in_apps = 0
    in_accounts = 0
    in_enrollments = 0

    app_matches = []
    for p in pending:
        em = p['email'].strip().lower()
        c.execute("SELECT id, name, email, status, domain, created_at FROM applications WHERE LOWER(email)=?", (em,))
        row_app = c.fetchone()
        if row_app:
            in_apps += 1
            app_matches.append((p, row_app))

        c.execute("SELECT id, name, email, is_active FROM intern_accounts WHERE LOWER(email)=?", (em,))
        row_acc = c.fetchone()
        if row_acc:
            in_accounts += 1

        c.execute("SELECT id, name, email, batch_label, payment_status FROM enrollments WHERE LOWER(email)=?", (em,))
        row_enr = c.fetchone()
        if row_enr:
            in_enrollments += 1

    conn.close()

    print(f"Results across {len(pending)} pending candidates:")
    print(f"  - Found in `applications` table: {in_apps}")
    print(f"  - Found in `intern_accounts` table: {in_accounts}")
    print(f"  - Found in `enrollments` table: {in_enrollments}")
    print("--------------------------------------------------")
    print("Sample application statuses:")
    status_counts = {}
    for p, app in app_matches:
        st = app[3]
        status_counts[st] = status_counts.get(st, 0) + 1
    for st, cnt in status_counts.items():
        print(f"  {st}: {cnt}")

if __name__ == '__main__':
    main()
