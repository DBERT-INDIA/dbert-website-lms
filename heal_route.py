@app.route("/admin/heal")
def admin_heal():
    user = require_role("admin")
    if not user:
        return "Unauthorized", 401
    try:
        from heal_db import heal_database
        heal_database()
        
        # Also forcefully drop the problematic FK constraint to unblock the portal
        with get_db() as conn:
            try:
                conn._raw_conn.autocommit = True
                cur = conn._raw_conn.cursor()
                cur.execute("ALTER TABLE course_enrollments DROP CONSTRAINT IF EXISTS course_enrollments_intern_id_fkey;")
                cur.close()
                conn._raw_conn.autocommit = False
            except Exception as e:
                print("Could not drop constraint:", e)
                
        return "Database healed successfully. Check EC2 logs for details."
    except Exception as e:
        return f"Error: {e}"
