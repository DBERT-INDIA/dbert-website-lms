import csv
import time
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import random
import re

DOMAINS = [
    "AI Agent Development",
    "Data Analyst",
    "Full Stack Development",
    "Python Automation"
]

def extract_metadata(title, url):
    company = "Unknown"
    company_match = re.search(r'(?i)at ([A-Za-z0-9\s]+)', title)
    if company_match:
        company = company_match.group(1).strip()
    
    location = "Remote" if "remote" in title.lower() or "remote" in url.lower() else "India"
    is_remote = "Yes" if location == "Remote" else "No"
        
    return company, location, is_remote

def run_scraper():
    all_results = []
    
    for domain in DOMAINS:
        domain_count = 0
        queries = [
            f"site:internshala.com \"{domain}\" internship",
            f"site:wellfound.com \"{domain}\" intern",
            f"site:linkedin.com/jobs \"{domain}\" intern"
        ]
        
        for query in queries:
            try:
                print(f"Searching: {query}")
                for url in search(query, num_results=70):
                    company, location, is_remote = extract_metadata(domain, url)
                    all_results.append({
                        "Domain": domain,
                        "Company": company,
                        "Role": f"{domain} Intern",
                        "Location": location,
                        "Is Remote": is_remote,
                        "Start Date": "Immediate",
                        "End Date / Duration": "3-6 Months",
                        "Stipend / Salary": "Unpaid / Variable",
                        "URL": url,
                        "Description": f"{domain} Internship Opportunity. Apply via link."
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

    output_path = r"c:\Users\user\Desktop\dbert-website-lms\master_internships_published.csv"
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Domain', 'Company', 'Role', 'Location', 'Is Remote', 'Start Date', 'End Date / Duration', 'Stipend / Salary', 'URL', 'Description']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)
        
    print(f"Total results saved: {len(all_results)}")

if __name__ == "__main__":
    run_scraper()
