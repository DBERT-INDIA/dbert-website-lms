import sys
content = open('apps/portal/app.py', 'r', encoding='utf-8').read()

new_api = '''
@app.route("/api/admin/sourcing-stats")
def api_admin_sourcing_stats():
    if not require_admin():
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    try:
        region_filter = request.args.get('region', 'India') # default to India
        
        with get_db() as conn:
            c = conn.cursor()
            
            # Helper to execute with region
            def query_region(sql):
                c.execute(sql, (region_filter,))
                return c.fetchall()
            
            domains = [{'domain': r[0], 'count': r[1]} for r in query_region('SELECT Domain, COUNT(*) as cnt FROM scraped_internships WHERE Region = ? GROUP BY Domain ORDER BY cnt DESC')]
            
            work_models = [{'model': r[0], 'count': r[1]} for r in query_region('SELECT Work_Model, COUNT(*) as cnt FROM scraped_internships WHERE Region = ? GROUP BY Work_Model')]
            
            stipends = [{'stipend': r[0], 'count': r[1]} for r in query_region('SELECT Stipend_Normalized, COUNT(*) as cnt FROM scraped_internships WHERE Region = ? GROUP BY Stipend_Normalized ORDER BY cnt DESC')]
            
            cities = [{'city': r[0], 'count': r[1]} for r in query_region('SELECT City, COUNT(*) as cnt FROM scraped_internships WHERE Region = ? AND Work_Model != \\'Remote\\' GROUP BY City ORDER BY cnt DESC LIMIT 10')]
            
            timeline = [{'month': r[0], 'count': r[1]} for r in query_region('SELECT substr(Start_Date, 1, 7) as month, COUNT(*) as cnt FROM scraped_internships WHERE Region = ? GROUP BY month ORDER BY month')]
            
            c.execute('SELECT COUNT(*) FROM scraped_internships WHERE Region = ?', (region_filter,))
            total = c.fetchone()[0]
            
            c.execute('SELECT id, Domain, Company, Role, Location, Work_Model, Start_Date, End_Date, Stipend_Normalized as stipend, Source, Region, URL, Clicks FROM scraped_internships WHERE Region = ? ORDER BY id DESC LIMIT 500', (region_filter,))
            jobs = []
            for r in c.fetchall():
                jobs.append({
                    'id': r[0], 'domain': r[1], 'company': r[2], 'role': r[3], 'location': r[4],
                    'work_model': r[5], 'start_date': r[6], 'end_date': r[7],
                    'stipend': r[8], 'source': r[9], 'region': r[10], 'url': r[11], 'clicks': r[12]
                })
                
        return jsonify({
            'status': 'success',
            'data': {
                'total': total,
                'domains': domains,
                'work_models': work_models,
                'stipends': stipends,
                'cities': cities,
                'timeline': timeline,
                'jobs': jobs
            }
        })
    except Exception as e:
        app_logger.error(f"Error fetching sourcing stats: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/admin/sourcing/click/<int:job_id>")
def admin_sourcing_click(job_id):
    if not require_admin():
        return redirect("/admin-login")
    try:
        with get_db() as conn:
            c = conn.cursor()
            c.execute('UPDATE scraped_internships SET Clicks = Clicks + 1 WHERE id = ?', (job_id,))
            c.execute('SELECT URL FROM scraped_internships WHERE id = ?', (job_id,))
            row = c.fetchone()
            if row:
                return redirect(row[0])
            return "Job not found", 404
    except Exception as e:
        return "Error: " + str(e), 500
'''

import re
pattern = re.compile(r'@app\.route\("/api/admin/sourcing-stats"\).*?return jsonify\(\{"status": "error", "message": str\(e\)\}\), 500', re.DOTALL)
if pattern.search(content):
    new_content = pattern.sub(new_api.strip(), content)
    with open('apps/portal/app.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Updated app.py successfully.')
else:
    print('Could not find pattern in app.py')
