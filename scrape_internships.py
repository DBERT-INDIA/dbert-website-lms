import csv
import time
import requests
from duckduckgo_search import DDGS
import re
import random

DOMAINS = [
    "AI Agent Development",
    "Data Analyst",
    "Full Stack Development",
    "Python Automation"
]

SITES = [
    "site:internshala.com",
    "site:wellfound.com",
    "site:indeed.com",
    "site:linkedin.com",
    "site:glassdoor.com",
    "site:remotive.com"
]

def extract_metadata(title, body, url):
    # Try to extract company
    company = "Unknown"
    company_match = re.search(r'(?i)at ([A-Za-z0-9\s]+)', title)
    if company_match:
        company = company_match.group(1).strip()
    
    # Try to extract location
    location = "Unknown"
    is_remote = "No"
    if "remote" in title.lower() or "remote" in body.lower() or "remote" in url.lower():
        is_remote = "Yes"
        location = "Remote"
        
    return company, location, is_remote

def run_scraper():
    all_results = []
    
    with DDGS() as ddgs:
        for domain in DOMAINS:
            domain_count = 0
            for site in SITES:
                query = f"{site} \"{domain}\" internship"
                try:
                    results = ddgs.text(query, max_results=40)
                    for r in results:
                        title = r.get("title", "")
                        body = r.get("body", "")
                        url = r.get("href", "")
                        
                        company, location, is_remote = extract_metadata(title, body, url)
                        
                        all_results.append({
                            "Domain": domain,
                            "Company": company,
                            "Role": title.replace(" - Internshala", "").replace(" | LinkedIn", ""),
                            "Location": location,
                            "Is Remote": is_remote,
                            "Start Date": "Immediate",
                            "End Date / Duration": "Unknown",
                            "Stipend / Salary": "Unpaid / Variable",
                            "URL": url,
                            "Description": body[:200]
                        })
                        domain_count += 1
                        if domain_count >= 200:
                            break
                    time.sleep(2)
                except Exception as e:
                    print(f"Error searching {query}: {e}")
                
                if domain_count >= 200:
                    break
            print(f"Collected {domain_count} for {domain}")

    # Write to CSV
    output_path = r"c:\Users\user\Desktop\dbert-website-lms\master_internships_published.csv"
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Domain', 'Company', 'Role', 'Location', 'Is Remote', 'Start Date', 'End Date / Duration', 'Stipend / Salary', 'URL', 'Description']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)
        
    print(f"Total results saved: {len(all_results)}")

if __name__ == "__main__":
    run_scraper()
