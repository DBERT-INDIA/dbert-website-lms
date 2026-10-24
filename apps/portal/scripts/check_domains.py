import sqlite3
conn = sqlite3.connect('apps/portal/internship.db')
c = conn.cursor()

print("--- posts domain counts ---")
for r in c.execute("SELECT domain, COUNT(*) FROM posts GROUP BY domain").fetchall():
    print(f"  {r[0]}: {r[1]}")

print("\n--- scraped_internships domain counts ---")
for r in c.execute("SELECT Domain, COUNT(*) FROM scraped_internships GROUP BY Domain").fetchall():
    print(f"  {r[0]}: {r[1]}")

print("\n--- scraped_internships Region x Domain ---")
for r in c.execute("SELECT Region, Domain, COUNT(*) FROM scraped_internships GROUP BY Region, Domain ORDER BY Region, Domain").fetchall():
    print(f"  {r[0]} | {r[1]}: {r[2]}")
