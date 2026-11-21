import os
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')
conn = psycopg2.connect(os.environ['DATABASE_URL'])
c = conn.cursor()

# 1. Check if table exists
c.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'gl_student_learning_profile' AND table_schema = 'dbert_internship';")
cols = c.fetchall()
print("gl_student_learning_profile columns:", cols)

c.execute("SELECT count(*) FROM dbert_internship.gl_student_learning_profile;")
cnt = c.fetchone()[0]
print(f"Total gl_student_learning_profile records: {cnt}")

# 2. Check sample row
c.execute("SELECT * FROM dbert_internship.gl_student_learning_profile LIMIT 3;")
rows = c.fetchall()
print("Sample gl_student_learning_profile rows:", rows)

# 3. Check course enrollments for Ratnadeep
c.execute("SELECT id, intern_id, email, course_id, current_day, completed_at FROM dbert_internship.course_enrollments WHERE LOWER(email) = 'ratnadeepratu737@gmail.com';")
enrs = c.fetchall()
print("Course enrollments for ratnadeepratu737@gmail.com:", enrs)

# 4. Check courses available
c.execute("SELECT id, title, slug, domain FROM dbert_internship.courses ORDER BY id;")
courses = c.fetchall()
print(f"Total courses: {len(courses)}")
for cs in courses[:5]:
    print("  Course:", cs)
