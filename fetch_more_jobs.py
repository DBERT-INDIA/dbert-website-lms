import csv
import json
import urllib.request
import re
import os
import time

CSV_FILE = r'c:\Users\user\Desktop\dbert-website-lms\extra_jobs.csv'

ai_keywords = ["ai ", "machine learning", "generative ai", "prompt engineer", "nlp", "llm", "deep learning", "ai researcher", "artificial intelligence", "ml engineer", "data scientist", "computer vision"]
python_keywords = ["python", "backend", "qa automation", "test automation", "devops", "site reliability", "sre", "data engineer", "django", "flask", "fastapi"]

ai_jobs = []
python_jobs = []
seen_urls = set()

def process_job(title, company, location, is_remote, url, desc, salary):
    if not url: return
    if url in seen_urls: return
    title_lower = title.lower()
    
    domain = None
    if any(k in title_lower for k in ai_keywords) or any(k in title_lower for k in ["artificial intelligence"]):
        domain = "AI Agent Development"
    elif any(k in title_lower for k in python_keywords):
        domain = "Python Automation"
        
    if domain:
        # Strip some html
        clean_desc = re.sub(r'<[^>]+>', '', str(desc))
        job_data = {
            "Domain": domain,
            "Company": company,
            "Role": title,
            "Location": location,
            "Is Remote": is_remote,
            "Start Date": "",
            "End Date / Duration": "",
            "Stipend / Salary": salary,
            "URL": url,
            "Description": clean_desc[:300].replace('\n', ' ').replace('\r', ' ')
        }
        if domain == "AI Agent Development":
            ai_jobs.append(job_data)
        else:
            python_jobs.append(job_data)
        seen_urls.add(url)

def fetch_remotive():
    url = "https://remotive.com/api/remote-jobs"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            for job in data.get('jobs', []):
                process_job(job.get('title', ''), job.get('company_name', ''), job.get('candidate_required_location', ''), "Yes", job.get('url', ''), job.get('description', ''), job.get('salary', ''))
    except Exception as e: print(e)

def fetch_arbeitnow():
    url = "https://www.arbeitnow.com/api/job-board-api"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            for job in data.get('data', []):
                process_job(job.get('title', ''), job.get('company_name', ''), job.get('location', ''), "Yes" if job.get('remote') else "No", job.get('url', ''), job.get('description', ''), "")
    except Exception as e: print(e)

def fetch_jobicy():
    url = "https://jobicy.com/api/v2/remote-jobs"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            for job in data.get('jobs', []):
                process_job(job.get('jobTitle', ''), job.get('companyName', ''), job.get('jobGeo', ''), "Yes", job.get('url', ''), job.get('jobDescription', ''), job.get('annualSalaryMin', ''))
    except Exception as e: print(e)

def fetch_himalayas():
    url = "https://himalayas.app/jobs/api"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            for job in data.get('jobs', []):
                process_job(job.get('title', ''), job.get('companyName', ''), job.get('locationRestrictions', [''])[0] if job.get('locationRestrictions') else '', "Yes", job.get('applicationLink', ''), job.get('excerpt', ''), "")
    except Exception as e: print(e)

fetch_remotive()
fetch_arbeitnow()
fetch_jobicy()
fetch_himalayas()

print(f"Got {len(ai_jobs)} AI jobs and {len(python_jobs)} Python jobs")

with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Domain", "Company", "Role", "Location", "Is Remote", "Start Date", "End Date / Duration", "Stipend / Salary", "URL", "Description"])
    writer.writeheader()
    for job in ai_jobs:
        writer.writerow(job)
    for job in python_jobs:
        writer.writerow(job)
