import sqlite3
import os

DB_PATH = 'apps/portal/internship.db'

def repair():
    if not os.path.exists(DB_PATH):
        print(f"Error: {DB_PATH} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Update college & academics in applications from intern_accounts
    update_academics_query = """
    UPDATE applications
    SET 
        college = (
            SELECT ia.college FROM intern_accounts ia 
            WHERE LOWER(ia.email) = LOWER(applications.email) 
            AND ia.college IS NOT NULL AND ia.college != '' AND ia.college != 'Student'
        ),
        city = COALESCE(
            (SELECT ia.city FROM intern_accounts ia WHERE LOWER(ia.email) = LOWER(applications.email) AND ia.city IS NOT NULL AND ia.city != ''),
            city
        ),
        course = COALESCE(
            (SELECT ia.course FROM intern_accounts ia WHERE LOWER(ia.email) = LOWER(applications.email) AND ia.course IS NOT NULL AND ia.course != ''),
            course
        ),
        semester = COALESCE(
            (SELECT ia.semester FROM intern_accounts ia WHERE LOWER(ia.email) = LOWER(applications.email) AND ia.semester IS NOT NULL AND ia.semester != ''),
            semester
        ),
        year_of_passing = COALESCE(
            (SELECT ia.year_of_passing FROM intern_accounts ia WHERE LOWER(ia.email) = LOWER(applications.email) AND ia.year_of_passing IS NOT NULL AND ia.year_of_passing != ''),
            year_of_passing
        ),
        updated_at = datetime('now', 'localtime')
    WHERE college = 'Student'
    AND EXISTS (
        SELECT 1 FROM intern_accounts ia 
        WHERE LOWER(ia.email) = LOWER(applications.email) 
        AND ia.college IS NOT NULL AND ia.college != '' AND ia.college != 'Student'
    );
    """
    cursor.execute(update_academics_query)
    repaired_academics = cursor.rowcount
    print(f"Restored academic details (real college names) for {repaired_academics} applications.")

    # 2. Update domain from intern_accounts (safely avoiding UNIQUE(email, domain) violations)
    cursor.execute("""
        SELECT a.id, a.email, a.domain AS current_domain, ia.domain AS target_domain
        FROM applications a
        JOIN intern_accounts ia ON LOWER(ia.email) = LOWER(a.email)
        WHERE ia.domain IS NOT NULL AND ia.domain != '' 
        AND ia.domain IN ('AI Agent Development', 'Data Analyst', 'Full Stack Development', 'Python Automation')
        AND ia.domain != a.domain
    """)
    mismatches = cursor.fetchall()
    repaired_domains_acct = 0
    for r in mismatches:
        # Check if an application already exists for this email with target_domain
        exists = cursor.execute(
            "SELECT id FROM applications WHERE LOWER(email) = LOWER(?) AND domain = ? AND id != ?",
            (r['email'], r['target_domain'], r['id'])
        ).fetchone()
        if not exists:
            cursor.execute(
                "UPDATE applications SET domain = ?, updated_at = datetime('now', 'localtime') WHERE id = ?",
                (r['target_domain'], r['id'])
            )
            repaired_domains_acct += 1
    print(f"Restored domain from account preferences for {repaired_domains_acct} applications.")

    # 3. For applications that are still 'AI Agent Development' but the intern applied to posts in another domain
    cursor.execute("""
        SELECT a.id, a.email, a.domain, p.domain AS post_domain
        FROM applications a
        JOIN intern_accounts ia ON LOWER(ia.email) = LOWER(a.email)
        JOIN post_applications pa ON pa.intern_id = ia.id
        JOIN posts p ON p.id = pa.post_id
        WHERE a.domain = 'AI Agent Development'
        AND p.domain != 'AI Agent Development'
        AND p.domain IN ('Data Analyst', 'Full Stack Development', 'Python Automation')
    """)
    post_mismatches = cursor.fetchall()
    updated_from_posts = 0
    for row in post_mismatches:
        exists = cursor.execute(
            "SELECT id FROM applications WHERE LOWER(email) = LOWER(?) AND domain = ? AND id != ?",
            (row['email'], row['post_domain'], row['id'])
        ).fetchone()
        if not exists:
            cursor.execute("UPDATE applications SET domain = ?, updated_at = datetime('now', 'localtime') WHERE id = ?", (row['post_domain'], row['id']))
            cursor.execute("UPDATE intern_accounts SET domain = ?, updated_at = datetime('now', 'localtime') WHERE LOWER(email) = LOWER(?)", (row['post_domain'], row['email']))
            updated_from_posts += 1
    print(f"Aligned domain based on job/internship post applications for {updated_from_posts} applications.")

    conn.commit()
    conn.close()
    print("Database restoration completed successfully!")

if __name__ == '__main__':
    repair()
