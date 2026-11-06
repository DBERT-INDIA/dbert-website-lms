import sqlite3
import json

conn = sqlite3.connect("apps/portal/internship.db")
c = conn.cursor()

with open("outputs/certificates_registry.json", "r", encoding="utf-8") as f:
    registry = json.load(f)

print(f"Total registry entries: {len(registry)}")

found_accounts = 0
found_apps = 0
found_enrollments = 0

for k, rec in registry.items():
    em = rec["email"]
    c.execute("SELECT id, name, email FROM intern_accounts WHERE email = ?", (em,))
    acc = c.fetchone()
    if acc:
        found_accounts += 1

    c.execute("SELECT id, name, email FROM applications WHERE email = ?", (em,))
    app = c.fetchone()
    if app:
        found_apps += 1

    c.execute("SELECT id, name, email FROM enrollments WHERE email = ?", (em,))
    enr = c.fetchone()
    if enr:
        found_enrollments += 1

print(f"Matching in intern_accounts: {found_accounts}/{len(registry)}")
print(f"Matching in applications: {found_apps}/{len(registry)}")
print(f"Matching in enrollments: {found_enrollments}/{len(registry)}")

# Check Kushal Agarwal specifically
c.execute("SELECT id, name, email, account_status, domain, tutor_completion_pct FROM intern_accounts WHERE email LIKE '%kushal%' OR name LIKE '%Kushal%'")
print("Kushal in intern_accounts:", c.fetchall())

conn.close()
