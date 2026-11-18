import subprocess
import json

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

remote_script = """
import psycopg2
import json

conn = psycopg2.connect("postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms")
c = conn.cursor()

# 1. Total opportunities by category
c.execute("SELECT count(*) FROM dbert_internship.scraped_internships")
total_scraped_internships = c.fetchone()[0]

c.execute("SELECT count(*) FROM dbert_internship.scraped_jobs")
total_scraped_jobs = c.fetchone()[0]

c.execute("SELECT post_type, count(*) FROM dbert_internship.posts GROUP BY post_type")
direct_posts_breakdown = dict(c.fetchall())

# 2. Domain breakdown for internships
c.execute(\"\"\"
SELECT domain, count(*) 
FROM dbert_internship.scraped_internships 
GROUP BY domain 
ORDER BY count(*) DESC
\"\"\")
internships_by_domain = c.fetchall()

# 3. Domain breakdown for jobs
c.execute(\"\"\"
SELECT domain, count(*) 
FROM dbert_internship.scraped_jobs 
GROUP BY domain 
ORDER BY count(*) DESC
\"\"\")
jobs_by_domain = c.fetchall()

# 4. Direct employer posts by domain
c.execute(\"\"\"
SELECT domain, post_type, count(*) 
FROM dbert_internship.posts 
GROUP BY domain, post_type 
ORDER BY domain, post_type
\"\"\")
direct_posts_domain = c.fetchall()

# 5. Work model breakdown
c.execute("SELECT work_model, count(*) FROM dbert_internship.scraped_internships GROUP BY work_model")
intern_work_model = dict(c.fetchall())

c.execute("SELECT work_model, count(*) FROM dbert_internship.scraped_jobs GROUP BY work_model")
job_work_model = dict(c.fetchall())

# 6. Direct posts work model
c.execute("SELECT work_mode, count(*) FROM dbert_internship.posts GROUP BY work_mode")
direct_work_mode = dict(c.fetchall())

# 7. Total companies & applications
c.execute("SELECT count(*) FROM dbert_internship.companies")
total_companies = c.fetchone()[0]

c.execute("SELECT count(*) FROM dbert_internship.post_applications")
total_applications_submitted = c.fetchone()[0]

c.execute("SELECT status, count(*) FROM dbert_internship.post_applications GROUP BY status")
application_statuses = dict(c.fetchall())

out = {
    "total_scraped_internships": total_scraped_internships,
    "total_scraped_jobs": total_scraped_jobs,
    "direct_posts_breakdown": direct_posts_breakdown,
    "internships_by_domain": internships_by_domain,
    "jobs_by_domain": jobs_by_domain,
    "direct_posts_domain": direct_posts_domain,
    "intern_work_model": intern_work_model,
    "job_work_model": job_work_model,
    "direct_work_mode": direct_work_mode,
    "total_companies": total_companies,
    "total_applications_submitted": total_applications_submitted,
    "application_statuses": application_statuses
}

print(json.dumps(out, indent=2))
"""

ssh_cmd = ["ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", REMOTE_HOST, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3"]
res = subprocess.run(ssh_cmd, input=remote_script, text=True, capture_output=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
