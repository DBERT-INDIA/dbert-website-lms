#!/usr/bin/env python3
"""
Comprehensive Audit:
1. Current Enrollments in PostgreSQL
2. Weekly Attendance & 10-Hour Goal Completion (Last Weeks)
3. Tracking Mechanisms: attendance, user_sessions, gl_learning_sessions, tutor_progress
4. Legacy SQLite vs PostgreSQL comparison
"""

import os
import sys
import sqlite3
import psycopg2
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')
conn = psycopg2.connect(os.environ['DATABASE_URL'])
c = conn.cursor()

print("=" * 70)
print("1. CURRENT ENROLLMENTS AUDIT (PostgreSQL: dbert_internship.enrollments)")
print("=" * 70)

c.execute("SELECT count(*) FROM enrollments;")
total_enr = c.fetchone()[0]
print(f"Total Enrollments: {total_enr}")

c.execute("""
    SELECT payment_status, count(*) 
    FROM enrollments 
    GROUP BY payment_status 
    ORDER BY count(*) DESC;
""")
print("\nBy Payment Status:")
for r in c.fetchall():
    print(f"  {r[0]}: {r[1]}")

c.execute("""
    SELECT batch_label, joining_date, count(*) 
    FROM enrollments 
    GROUP BY batch_label, joining_date 
    ORDER BY count(*) DESC LIMIT 10;
""")
print("\nTop Batches / Joining Dates:")
for r in c.fetchall():
    print(f"  {r[0]} (JD: {r[1]}): {r[2]}")

c.execute("""
    SELECT product, amount, deposit_paid, count(*) 
    FROM enrollments 
    GROUP BY product, amount, deposit_paid 
    ORDER BY count(*) DESC;
""")
print("\nBy Product / Amount / Deposit Paid:")
for r in c.fetchall():
    print(f"  Product: {r[0]} | Amount: {r[1]} | Deposit Paid: {r[2]} -> {r[3]}")

print("\n" + "=" * 70)
print("2. ATTENDANCE & 10-HOUR (600 MIN) COMPLETION (PostgreSQL: attendance)")
print("=" * 70)

c.execute("SELECT count(*), count(DISTINCT intern_id), count(DISTINCT email) FROM attendance;")
att_stats = c.fetchone()
print(f"Total attendance records: {att_stats[0]}")
print(f"Distinct intern_ids: {att_stats[1]}")
print(f"Distinct emails: {att_stats[2]}")

c.execute("""
    SELECT week_start, week_end, 
           count(*) as total_active_users,
           sum(CASE WHEN total_minutes >= 600 THEN 1 ELSE 0 END) as completed_10h,
           sum(CASE WHEN total_minutes >= 300 AND total_minutes < 600 THEN 1 ELSE 0 END) as between_5h_and_10h,
           sum(CASE WHEN total_minutes < 300 THEN 1 ELSE 0 END) as below_5h,
           max(total_minutes) as max_minutes,
           avg(total_minutes) as avg_minutes
    FROM attendance
    GROUP BY week_start, week_end
    ORDER BY week_start DESC
    LIMIT 12;
""")
print("\nWeekly Attendance Breakdown (10h = 600+ mins):")
print(f"{'Week Start':<12} | {'Week End':<12} | {'Active Users':<12} | {'Completed >=10h':<16} | {'5h-10h':<8} | {'<5h':<8} | {'Max Mins':<10} | {'Avg Mins':<10}")
print("-" * 95)
for r in c.fetchall():
    print(f"{r[0]:<12} | {r[1]:<12} | {r[2]:<12} | {r[3]:<16} | {r[4]:<8} | {r[5]:<8} | {r[6]:<10} | {round(r[7] or 0, 1):<10}")

c.execute("""
    SELECT a.intern_id, a.email, ia.name, a.week_start, a.total_minutes, round(a.total_minutes/60.0, 1) as hours
    FROM attendance a
    LEFT JOIN intern_accounts ia ON ia.id = a.intern_id
    WHERE a.total_minutes >= 600
    ORDER BY a.week_start DESC, a.total_minutes DESC
    LIMIT 20;
""")
print("\nSample Interns Completing >= 10 Hours:")
for r in c.fetchall():
    print(f"  Week {r[3]}: Intern #{r[0]} ({r[2]} | {r[1]}) -> {r[4]} mins ({r[5]} hrs)")

print("\n" + "=" * 70)
print("3. OTHER TRACKING TABLES (user_sessions, tutor, guided learning)")
print("=" * 70)

c.execute("SELECT count(*) FROM user_sessions;")
print(f"Total user_sessions: {c.fetchone()[0]}")

c.execute("SELECT count(*) FROM tutor_progress;")
print(f"Total tutor_progress: {c.fetchone()[0]}")

c.execute("SELECT count(*) FROM gl_learning_sessions;")
print(f"Total gl_learning_sessions: {c.fetchone()[0]}")

c.execute("""
    SELECT count(*), 
           sum(CASE WHEN tutor_seconds_credited > 0 THEN 1 ELSE 0 END) as has_seconds,
           max(tutor_seconds_credited)
    FROM intern_accounts;
""")
ia_tutor = c.fetchone()
print(f"Intern accounts with tutor_seconds_credited > 0: {ia_tutor[1]} / {ia_tutor[0]} (max: {ia_tutor[2]}s)")

print("\n" + "=" * 70)
print("4. LEGACY SQLITE TRACKING (internship.db / portal.db on EC2)")
print("=" * 70)

sqlite_paths = [
    '/var/www/dbert-website-lms/apps/portal/internship.db',
    '/var/www/dbert-website-lms/apps/portal/portal.db',
    '/var/www/dbert-website-lms/apps/portal/dbert.db',
    '/var/www/dbert-website-lms/apps/portal/dbert_lms.db'
]

for p in sqlite_paths:
    if os.path.exists(p):
        size_mb = os.path.getsize(p) / (1024 * 1024)
        print(f"\nSQLite File: {p} ({size_mb:.2f} MB)")
        try:
            s_conn = sqlite3.connect(p)
            sc = s_conn.cursor()
            sc.execute("SELECT name FROM sqlite_master WHERE type='table';")
            s_tables = [row[0] for row in sc.fetchall()]
            print(f"  Tables ({len(s_tables)}): {', '.join(s_tables[:15])}...")
            
            for check_t in ['attendance', 'enrollments', 'user_sessions', 'study_sessions', 'tutor_progress']:
                if check_t in s_tables:
                    sc.execute(f"SELECT count(*) FROM {check_t};")
                    cnt = sc.fetchone()[0]
                    print(f"    Table '{check_t}': {cnt} rows")
                    if check_t == 'attendance' and cnt > 0:
                        sc.execute("SELECT week_start, count(*), sum(CASE WHEN total_minutes>=600 THEN 1 ELSE 0 END) FROM attendance GROUP BY week_start ORDER BY week_start DESC LIMIT 5;")
                        print("    Legacy SQLite Attendance summary:")
                        for w in sc.fetchall():
                            print(f"      Week {w[0]}: {w[1]} records, {w[2]} completed >= 10h")
            s_conn.close()
        except Exception as e:
            print(f"  Error reading {p}: {e}")
    else:
        print(f"\nSQLite File {p} DOES NOT EXIST.")

c.close()
conn.close()
