import sqlite3
import re
import math

db_path = 'apps/portal/internship.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute("SELECT id, Location, Is_Remote, Stipend FROM scraped_internships")
rows = c.fetchall()

def extract_numbers(text):
    # Find all numeric parts, handling 'k'
    text = text.lower().replace(',', '')
    matches = re.findall(r'[\d\.]+(?:k)?', text)
    nums = []
    for m in matches:
        if m.endswith('k'):
            try: nums.append(float(m[:-1]) * 1000)
            except: pass
        else:
            try: nums.append(float(m))
            except: pass
    return nums

def normalize_stipend(stipend):
    if not stipend or 'not disclosed' in stipend.lower(): return 'Not Disclosed'
    if 'unpaid' in stipend.lower(): return 'Unpaid'
    
    stipend = stipend.lower()
    is_hourly = '/hour' in stipend or ' hr' in stipend or 'hourly' in stipend
    
    multiplier = 1
    if '$' in stipend or 'usd' in stipend:
        multiplier = 84
    elif '€' in stipend or 'eur' in stipend:
        multiplier = 90
    elif '£' in stipend or 'gbp' in stipend:
        multiplier = 110
    else:
        multiplier = 1 # Assume INR if no currency symbol or ₹ is present
        
    nums = extract_numbers(stipend)
    if not nums: return 'Not Disclosed'
    
    # Convert to monthly INR
    inr_nums = []
    for n in nums:
        if n < 10 and not is_hourly: 
            n = n * 100000 # probably meant Lakhs, but let's assume it's just raw if it's small. Wait, $90k has k handled. If it's ₹ 5, it means nothing.
        
        val = n * multiplier
        if is_hourly:
            val = val * 160 # 160 hours a month
        elif val > 10000000: # yearly? If it's > 1 crore INR, it's probably yearly
            val = val / 12
        elif val > 1000000 and multiplier > 1: # $100k yearly
            val = val / 12
            
        inr_nums.append(val)
        
    avg = sum(inr_nums) / len(inr_nums)
    
    if avg < 10000: return '< ₹10,000 /month'
    if avg <= 30000: return '₹10,000 - ₹30,000 /month'
    if avg <= 50000: return '₹30,000 - ₹50,000 /month'
    if avg <= 100000: return '₹50,000 - ₹1,00,000 /month'
    return '> ₹1,00,000 /month'

def parse_location(location, is_remote):
    location = str(location) if location else ""
    loc_lower = location.lower()
    
    # Determine Work Model
    if 'hybrid' in loc_lower:
        model = 'Hybrid'
    elif 'remote' in loc_lower or 'homeoffice' in loc_lower or is_remote == 'Yes':
        model = 'Remote' if 'und' not in loc_lower and 'and' not in loc_lower else 'Hybrid'
    else:
        model = 'Onsite'
        
    # Determine City
    city = 'Unknown'
    if model != 'Remote':
        # Split by comma and take first
        parts = location.split(',')
        if parts:
            city = parts[0].strip()
            # Clean up
            city = re.sub(r'(?i)greater | area| metropolitan', '', city).strip()
            
    return model, city

updates = []
for r in rows:
    stipend_norm = normalize_stipend(r['Stipend'])
    model, city = parse_location(r['Location'], r['Is_Remote'])
    updates.append((stipend_norm, model, city, r['id']))

c.executemany("UPDATE scraped_internships SET Stipend_Normalized=?, Work_Model=?, City=? WHERE id=?", updates)
conn.commit()
print(f"Updated {len(updates)} records.")
conn.close()
