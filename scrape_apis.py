import csv
import requests
import re
import time

DOMAINS = [
    "AI Agent Development",
    "Data Analyst",
    "Full Stack Development",
    "Python Automation"
]

def map_domain(title, desc):
    title = title.lower()
    desc = desc.lower()
    
    if "data" in title or "data" in desc or "analyst" in title:
        return "Data Analyst"
    if "full stack" in title or "fullstack" in title or "web" in title:
        return "Full Stack Development"
    if "python" in title or "automation" in title:
        return "Python Automation"
    if "ai " in title or "machine learning" in title or "agent" in title:
        return "AI Agent Development"
    
    return "Full Stack Development" # Fallback

def run_api_scraper():
    all_results = []
    
    # 1. Arbeitnow API
    print("Fetching from Arbeitnow API...")
    for page in range(1, 10):
        try:
            r = requests.get(f"https://www.arbeitnow.com/api/job-board-api?page={page}", timeout=10)
            if r.status_code == 200:
                data = r.json().get("data", [])
                for job in data:
                    title = job.get("title", "")
                    desc = job.get("description", "")
                    
                    domain = map_domain(title, desc)
                    
                    all_results.append({
                        "Domain": domain,
                        "Company": job.get("company_name", "Unknown"),
                        "Role": title,
                        "Location": job.get("location", "Global"),
                        "Is Remote": "Yes" if job.get("remote") else "No",
                        "Start Date": job.get("created_at", "Immediate"),
                        "End Date / Duration": "N/A",
                        "Stipend / Salary": "Unknown",
                        "URL": job.get("url", ""),
                        "Description": re.sub('<[^<]+>', '', desc)[:200]
                    })
        except Exception as e:
            print(f"Arbeitnow error: {e}")
            
    # 2. Remotive API
    print("Fetching from Remotive API...")
    try:
        r = requests.get("https://remotive.com/api/remote-jobs", timeout=10)
        if r.status_code == 200:
            data = r.json().get("jobs", [])
            for job in data:
                title = job.get("title", "")
                desc = job.get("description", "")
                
                domain = map_domain(title, desc)
                
                all_results.append({
                    "Domain": domain,
                    "Company": job.get("company_name", "Unknown"),
                    "Role": title,
                    "Location": job.get("candidate_required_location", "Remote"),
                    "Is Remote": "Yes",
                    "Start Date": job.get("publication_date", "Immediate"),
                    "End Date / Duration": "N/A",
                    "Stipend / Salary": job.get("salary", "Unknown"),
                    "URL": job.get("url", ""),
                    "Description": re.sub('<[^<]+>', '', desc)[:200]
                })
    except Exception as e:
        print(f"Remotive error: {e}")

    # Write to CSV
    output_path = r"c:\Users\user\Desktop\dbert-website-lms\master_internships_published.csv"
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Domain', 'Company', 'Role', 'Location', 'Is Remote', 'Start Date', 'End Date / Duration', 'Stipend / Salary', 'URL', 'Description']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)
        
    print(f"Total results saved: {len(all_results)}")
    
    # Print counts per domain
    counts = {d: 0 for d in DOMAINS}
    for r in all_results:
        if r["Domain"] in counts:
            counts[r["Domain"]] += 1
    for d, c in counts.items():
        print(f"{d}: {c}")

if __name__ == "__main__":
    run_api_scraper()
