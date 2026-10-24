import requests
import csv
import os
import json
import time

domains = [
    "AI Agent Development",
    "Data Analyst",
    "Full Stack Development",
    "Python Automation"
]

jobs = []

def fetch_remotive():
    try:
        url = "https://remotive.com/api/remote-jobs?limit=1000"
        r = requests.get(url)
        data = r.json()
        for j in data.get("jobs", []):
            title = j.get("title", "").lower()
            company = j.get("company_name", "")
            location = j.get("candidate_required_location", "Remote")
            url = j.get("url", "")
            description = str(j.get("description", ""))[:200]
            
            domain = None
            if "data" in title and ("analyst" in title or "analy" in title):
                domain = "Data Analyst"
            elif "full stack" in title or "fullstack" in title:
                domain = "Full Stack Development"
            elif "python" in title:
                domain = "Python Automation"
            elif "ai" in title or "machine learning" in title or "ml" in title or "artificial intelligence" in title:
                domain = "AI Agent Development"
            else:
                # If not matched strictly, try to match by keywords in description for some others
                desc_lower = description.lower()
                if "python" in desc_lower and ("automation" in desc_lower or "script" in desc_lower):
                    domain = "Python Automation"
                elif "full stack" in desc_lower:
                    domain = "Full Stack Development"
                elif "data analyst" in desc_lower:
                    domain = "Data Analyst"
                elif "ai agent" in desc_lower:
                    domain = "AI Agent Development"

            if domain:
                jobs.append({
                    "Domain": domain,
                    "Company": company,
                    "Role": j.get("title", ""),
                    "Location": location,
                    "Is Remote": "Yes",
                    "URL": url,
                    "Description": description.replace('\n', ' ').replace('\r', '').replace('<p>', '').replace('</p>', '').replace('<br>', '')
                })
    except Exception as e:
        print(f"Error fetching remotive: {e}")

def fetch_arbeitnow():
    try:
        url = "https://www.arbeitnow.com/api/job-board-api"
        for page in range(1, 10):
            r = requests.get(f"{url}?page={page}")
            if r.status_code != 200:
                break
            data = r.json()
            for j in data.get("data", []):
                title = j.get("title", "").lower()
                company = j.get("company_name", "")
                location = j.get("location", "Unknown")
                is_remote = "Yes" if j.get("remote") else "No"
                job_url = j.get("url", "")
                description = str(j.get("description", ""))[:200]
                
                domain = None
                if "data" in title and ("analyst" in title or "analy" in title):
                    domain = "Data Analyst"
                elif "full stack" in title or "fullstack" in title:
                    domain = "Full Stack Development"
                elif "python" in title:
                    domain = "Python Automation"
                elif "ai" in title or "machine learning" in title or "ml" in title or "artificial intelligence" in title:
                    domain = "AI Agent Development"
                    
                if domain:
                    jobs.append({
                        "Domain": domain,
                        "Company": company,
                        "Role": j.get("title", ""),
                        "Location": location,
                        "Is Remote": is_remote,
                        "URL": job_url,
                        "Description": description.replace('\n', ' ').replace('\r', '').replace('<p>', '').replace('</p>', '').replace('<br>', '')
                    })
            time.sleep(0.5)
    except Exception as e:
        print(f"Error fetching arbeitnow: {e}")

fetch_remotive()
fetch_arbeitnow()

csv_path = r"c:\Users\user\Desktop\dbert-website-lms\internships_sourced.csv"
os.makedirs(os.path.dirname(csv_path), exist_ok=True)

# Keep only unique jobs
unique_jobs = []
seen = set()
for j in jobs:
    if j['URL'] not in seen:
        seen.add(j['URL'])
        unique_jobs.append(j)

with open(csv_path, "w", newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Domain", "Company", "Role", "Location", "Is Remote", "URL", "Description"])
    writer.writeheader()
    writer.writerows(unique_jobs)

print(f"Saved {len(unique_jobs)} jobs to {csv_path}")
