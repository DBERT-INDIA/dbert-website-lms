import os
import csv
import datetime
import requests
import time
import re

DOMAINS = {
    "AI Agent Development": ["artificial intelligence", "generative ai", "ai agent", "machine learning"],
    "Data Analyst": ["data analyst", "data science", "data analytics"],
    "Full Stack Development": ["full stack", "web development", "backend", "frontend"],
    "Python Automation": ["python", "rpa", "automation", "quality assurance"]
}

CSV_FILE = 'indian_master_internships.csv'

def append_to_csv(data):
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def is_remote(loc_type, locations):
    if loc_type and 'wfh' in loc_type.lower():
        return 'Yes'
    if locations:
        for l in locations:
            if 'remote' in l.lower() or 'home' in l.lower():
                return 'Yes'
    return 'No'

def scrape_unstop():
    total_count = 0
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'application/json, text/plain, */*'
    }
    
    for domain, keywords in DOMAINS.items():
        for keyword in keywords:
            print(f"Searching Unstop for: {keyword}")
            page_num = 1
            max_pages = 5 
            
            while page_num <= max_pages:
                url = f"https://unstop.com/api/public/opportunity/search-result?opportunity=internships&keyword={keyword}&page={page_num}&per_page=30"
                
                try:
                    res = requests.get(url, headers=headers, timeout=10)
                    if res.status_code != 200:
                        break
                    
                    data = res.json().get('data', {}).get('data', [])
                    if not data:
                        break
                    
                    for item in data:
                        title = item.get('title', '')
                        
                        org_data = item.get('organisation')
                        company = org_data.get('name', '') if isinstance(org_data, dict) else str(org_data)
                        
                        seo_url = item.get('seo_url', '')
                        
                        job_detail = item.get('jobDetail', {})
                        if not job_detail: job_detail = {}
                        loc_type = job_detail.get('type', '')
                        locs = job_detail.get('locations', [])
                        
                        location_str = ", ".join(locs) if locs else ("Remote (India)" if loc_type == 'wfh' else "India")
                        remote_flag = is_remote(loc_type, locs)
                        
                        min_sal = job_detail.get('min_salary')
                        max_sal = job_detail.get('max_salary')
                        curr_raw = job_detail.get('currency')
                        curr = curr_raw.replace('fa-rupee', 'INR') if curr_raw else 'INR'
                        
                        stipend = "Not Disclosed"
                        if min_sal and max_sal:
                            stipend = f"{curr} {min_sal} - {max_sal}"
                        elif max_sal:
                            stipend = f"{curr} {max_sal}"
                        elif min_sal:
                            stipend = f"{curr} {min_sal}"
                            
                        start_date = today
                        end_dt = item.get('end_date')
                        duration = end_dt[:10] if end_dt else (datetime.datetime.now() + datetime.timedelta(days=90)).strftime('%Y-%m-%d')
                        
                        description = item.get('details', '')
                        if description:
                            description = re.sub('<[^<]+>', '', description).strip()[:200]
                        else:
                            description = f"Unstop Listing: {title} at {company}"
                            
                        if title and company:
                            append_to_csv([domain, company, title, location_str, remote_flag, start_date, duration, stipend, seo_url, description])
                            total_count += 1
                except Exception as e:
                    print(f"Error fetching Unstop page {page_num} for {keyword}: {e}")
                    break
                
                page_num += 1
                time.sleep(1)
                
    return total_count

if __name__ == "__main__":
    print(f"Starting Unstop Scraping...")
    c = scrape_unstop()
    print(f"Unstop Scraping complete! Total appended: {c}")
