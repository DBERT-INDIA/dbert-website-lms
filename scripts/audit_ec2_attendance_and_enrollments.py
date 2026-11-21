import os
import json
import psycopg2
from dotenv import load_dotenv
from datetime import datetime, date

load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')
conn = psycopg2.connect(os.environ['DATABASE_URL'])
c = conn.cursor()

report = {
    "timestamp": datetime.now().isoformat(),
    "enrollments": {},
    "attendance": {},
    "anomalies": []
}

# 1. Audit Enrollments
c.execute("SELECT count(*) FROM dbert_internship.enrollments;")
total_enr = c.fetchone()[0]

c.execute("""
    SELECT COALESCE(payment_status, 'NULL'), count(*)
    FROM dbert_internship.enrollments
    GROUP BY payment_status
    ORDER BY count(*) DESC;
""")
enr_by_status = dict(c.fetchall())

c.execute("""
    SELECT COALESCE(batch_label, 'No Batch'), count(*)
    FROM dbert_internship.enrollments
    GROUP BY batch_label
    ORDER BY count(*) DESC
    LIMIT 10;
""")
enr_by_batch = dict(c.fetchall())

report["enrollments"] = {
    "total_records": total_enr,
    "by_status": enr_by_status,
    "top_batches": enr_by_batch
}

# 2. Audit Attendance
c.execute("SELECT count(*) FROM dbert_internship.attendance;")
total_att = c.fetchone()[0]

c.execute("SELECT count(DISTINCT intern_id) FROM dbert_internship.attendance;")
distinct_interns = c.fetchone()[0]

c.execute("""
    SELECT week_start, count(*), sum(total_minutes),
           sum(CASE WHEN total_minutes >= 600 THEN 1 ELSE 0 END) as compliant_10h,
           max(total_minutes) as max_mins,
           round(avg(total_minutes), 1) as avg_mins
    FROM dbert_internship.attendance
    GROUP BY week_start
    ORDER BY week_start DESC
    LIMIT 8;
""")
recent_weeks = []
for r in c.fetchall():
    recent_weeks.append({
        "week_start": str(r[0]),
        "active_interns": r[1],
        "total_mins_cohort": int(r[2] or 0),
        "compliant_10h_count": r[3],
        "max_mins": r[4],
        "avg_mins": float(r[5] or 0)
    })

# Check for anomalies: duplicates on (intern_id, week_start)
c.execute("""
    SELECT intern_id, week_start, count(*)
    FROM dbert_internship.attendance
    GROUP BY intern_id, week_start
    HAVING count(*) > 1;
""")
dups = c.fetchall()
if dups:
    report["anomalies"].append(f"Found {len(dups)} duplicate (intern_id, week_start) rows in attendance!")
else:
    report["attendance_duplicates"] = 0

# Check for negative minutes or null total_minutes
c.execute("SELECT count(*) FROM dbert_internship.attendance WHERE total_minutes < 0 OR total_minutes IS NULL;")
neg_null = c.fetchone()[0]
if neg_null > 0:
    report["anomalies"].append(f"Found {neg_null} attendance rows with negative or null total_minutes!")

report["attendance"] = {
    "total_records": total_att,
    "distinct_interns": distinct_interns,
    "recent_weeks": recent_weeks,
    "duplicates": len(dups),
    "negative_or_null_minutes": neg_null
}

print(json.dumps(report, indent=2))

output_path = "/var/www/dbert-website-lms/data/attendance_enrollments_audit_report.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

print(f"\nAudit report saved to: {output_path}")
