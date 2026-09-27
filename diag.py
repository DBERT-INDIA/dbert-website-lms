@app.route("/admin/diag")
def admin_diag():
    import json
    try:
        with get_db() as conn:
            acct = conn.execute("SELECT * FROM intern_accounts WHERE id=3167").fetchone()
            acct_data = dict(acct) if acct else None
            
            fks = conn.execute("""
                SELECT conname, pg_get_constraintdef(c.oid) as condef
                FROM pg_constraint c
                JOIN pg_class t ON c.conrelid = t.oid
                WHERE t.relname = 'course_enrollments' AND contype = 'f';
            """).fetchall()
            
            acct2 = conn.execute("SELECT * FROM intern_accounts WHERE id=5046").fetchone()
            acct2_data = dict(acct2) if acct2 else None

            return json.dumps({
                "fks": [dict(f) for f in fks],
                "row_3167": acct_data,
                "row_5046": acct2_data
            }, default=str)
    except Exception as e:
        return str(e)
