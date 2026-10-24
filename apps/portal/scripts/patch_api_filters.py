import sys
content = open('apps/portal/app.py', 'r', encoding='utf-8').read()

new_api = '''
@app.route("/api/admin/sourcing-stats")
def api_admin_sourcing_stats():
    if not require_admin():
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    try:
        region_filter = request.args.get('region', 'India')
        domain_filter = request.args.get('domain', '')
        model_filter = request.args.get('work_model', '')
        
        where_clauses = ["Region = ?"]
        args = [region_filter]
        
        if domain_filter:
            where_clauses.append("Domain = ?")
            args.append(domain_filter)
        if model_filter:
            where_clauses.append("Work_Model = ?")
            args.append(model_filter)
            
        where_sql = " AND ".join(where_clauses)
        
        with get_db() as conn:
            c = conn.cursor()
            
            def query_filtered(select_sql, group_by="", order_by="", limit=""):
                full_sql = f"{select_sql} WHERE {where_sql} {group_by} {order_by} {limit}"
                c.execute(full_sql, tuple(args))
                return c.fetchall()
            
            domains = [{'domain': r[0], 'count': r[1]} for r in query_filtered('SELECT Domain, COUNT(*) as cnt FROM scraped_internships', 'GROUP BY Domain', 'ORDER BY cnt DESC')]
            
            work_models = [{'model': r[0], 'count': r[1]} for r in query_filtered('SELECT Work_Model, COUNT(*) as cnt FROM scraped_internships', 'GROUP BY Work_Model')]
            
            stipends = [{'stipend': r[0], 'count': r[1]} for r in query_filtered('SELECT Stipend_Normalized, COUNT(*) as cnt FROM scraped_internships', 'GROUP BY Stipend_Normalized', 'ORDER BY cnt DESC')]
            
            # For cities, exclude Remote unless the user explicitly filtered for Remote (which would make this empty)
            cities_sql = f"SELECT City, COUNT(*) as cnt FROM scraped_internships WHERE {where_sql} AND Work_Model != 'Remote' GROUP BY City ORDER BY cnt DESC LIMIT 10"
            c.execute(cities_sql, tuple(args))
            cities = [{'city': r[0], 'count': r[1]} for r in c.fetchall()]
            
            c.execute(f"SELECT COUNT(*) FROM scraped_internships WHERE {where_sql}", tuple(args))
            total = c.fetchone()[0]
            
            jobs_sql = f"SELECT id, Domain, Company, Role, Location, Work_Model, Start_Date, End_Date, Stipend_Normalized as stipend, Source, Region, URL, Clicks FROM scraped_internships WHERE {where_sql} ORDER BY id DESC LIMIT 500"
            c.execute(jobs_sql, tuple(args))
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
                'jobs': jobs
            }
        })
    except Exception as e:
        app_logger.error(f"Error fetching sourcing stats: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
'''

import re
# We need to replace the api_admin_sourcing_stats.
pattern = re.compile(r'@app\.route\("/api/admin/sourcing-stats"\).*?return jsonify\(\{"status": "error", "message": str\(e\)\}\), 500', re.DOTALL)
if pattern.search(content):
    new_content = pattern.sub(new_api.strip(), content)
    with open('apps/portal/app.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Updated app.py successfully with filters.')
else:
    print('Could not find pattern in app.py')
