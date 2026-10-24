import sqlite3
conn = sqlite3.connect('apps/portal/internship.db')
c = conn.cursor()
r1 = c.execute("SELECT COUNT(*) FROM scraped_internships WHERE Work_Model='Remote' OR Is_Remote='Yes' OR Location LIKE '%Remote%' OR City LIKE '%Remote%'").fetchone()[0]
print("Scraped leads matching Remote:", r1)
r2 = c.execute("SELECT COUNT(*) FROM scraped_internships WHERE City='Remote' OR Location LIKE '%Remote%'").fetchone()[0]
print("Scraped leads with City=Remote or Location like Remote:", r2)
r3 = c.execute("SELECT COUNT(*) FROM scraped_internships WHERE Domain='Data Analyst' AND (Work_Model='Remote' OR Is_Remote='Yes' OR Location LIKE '%Remote%' OR City LIKE '%Remote%')").fetchone()[0]
print("Scraped Data Analyst + Remote:", r3)
r4 = c.execute("SELECT COUNT(*) FROM posts WHERE domain='Data Analyst' AND (location='Remote' OR work_mode='Remote')").fetchone()[0]
print("Canonical Data Analyst + Remote:", r4)
