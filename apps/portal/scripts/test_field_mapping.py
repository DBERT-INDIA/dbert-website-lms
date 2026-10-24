import sqlite3, re
from datetime import datetime

db = sqlite3.connect('apps/portal/internship.db')
db.row_factory = sqlite3.Row
c = db.cursor()

c.execute("SELECT id, Role, Company, Location, Work_Model, Start_Date, End_Date, Stipend, Stipend_Normalized, Description FROM scraped_internships WHERE Stipend != 'Not Disclosed' LIMIT 5")
rows = list(c.fetchall())
c.execute("SELECT id, Role, Company, Location, Work_Model, Start_Date, End_Date, Stipend, Stipend_Normalized, Description FROM scraped_internships WHERE Stipend = 'Not Disclosed' LIMIT 5")
rows += list(c.fetchall())

for r in rows:
    dur = '3 Months'
    try:
        sd = datetime.strptime(r['Start_Date'][:10], '%Y-%m-%d')
        ed = datetime.strptime(r['End_Date'][:10], '%Y-%m-%d')
        days = (ed - sd).days
        if days <= 35: dur = '1 Month'
        elif days <= 65: dur = '2 Months'
        elif days <= 110: dur = '3 Months'
        else: dur = f"{round(days/30)} Months"
    except Exception:
        pass
    
    txt = (r['Role'] + ' ' + (r['Description'] or '')).lower()
    m = re.search(r'(\d+\s*(?:to|-)\s*\d+\s*(?:hours|hrs)(?:\s*(?:per|\/)\s*(?:week|wk))?|\d+\s*(?:hours|hrs)(?:\s*(?:per|\/)\s*(?:week|wk))?)', txt)
    if m:
        ht, hs = m.group(1).title(), 'As per job listing'
    elif 'part time' in txt or 'part-time' in txt:
        ht, hs = 'Part-Time', '15–20 Hours / Week'
    elif 'full time' in txt or 'full-time' in txt:
        ht, hs = 'Full-Time', '35–40 Hours / Week'
    elif r['Work_Model'] == 'Remote':
        ht, hs = 'Flexible Hours', 'Milestone & task based'
    else:
        ht, hs = 'Standard Working Hours', 'Full-time schedule'
    
    s = (r['Stipend'] or '').strip()
    sn = (r['Stipend_Normalized'] or '').strip()
    if s and s != 'Not Disclosed':
        st, ss = s, 'Offered by host company'
    elif sn and sn != 'Not Disclosed':
        st, ss = sn, 'Estimated industry bracket'
    else:
        st, ss = 'Performance Stipend', 'Disclosed upon interview'
        
    print(f"Job {r['id']}: {r['Role'][:25]} | Dur: {dur} | Hours: {ht} ({hs}) | Stipend: {st[:25]}")
