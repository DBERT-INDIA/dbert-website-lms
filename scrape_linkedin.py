import requests
from bs4 import BeautifulSoup
import csv
import time

domains = [
    ("AI Agent Development", "AI Intern"),
    ("Data Analyst", "Data Analyst Intern"),
    ("Full Stack Development", "Full Stack Intern"),
    ("Python Automation", "Python Intern")
]

output_file = r'c:\Users\user\Desktop\dbert-website-lms\indian_internships_sourced.csv'

def scrape_linkedin(domain_name, keywords):
    results = []
    # Fetch a couple of pages
    for start in [0, 25, 50, 75]:
        url = f"https://in.linkedin.com/jobs/search?keywords={keywords.replace(' ', '%20')}&location=India&start={start}"
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            jobs = soup.find_all('div', class_='base-card')
            
            for job in jobs:
                title_tag = job.find('h3', class_='base-search-card__title')
                company_tag = job.find('h4', class_='base-search-card__subtitle')
                location_tag = job.find('span', class_='job-search-card__location')
                link_tag = job.find('a', class_='base-card__full-link')
                
                if title_tag and company_tag and location_tag and link_tag:
                    title = title_tag.text.strip()
                    company = company_tag.text.strip()
                    location = location_tag.text.strip()
                    link = link_tag['href'].split('?')[0]
                    
                    is_remote = "Yes" if "remote" in location.lower() or "remote" in title.lower() else "No"
                    
                    results.append({
                        "Domain": domain_name,
                        "Company": company,
                        "Role": title,
                        "Location": location,
                        "Is Remote": is_remote,
                        "URL": link,
                        "Description": f"{title} role at {company} located in {location}."
                    })
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            
        time.sleep(2)
        
    return results

all_data = []
for domain_name, kw in domains:
    print(f"Scraping {domain_name} with keywords {kw}...")
    jobs = scrape_linkedin(domain_name, kw)
    
    # deduplicate
    seen = set()
    uniq = []
    for j in jobs:
        if j['URL'] not in seen:
            seen.add(j['URL'])
            uniq.append(j)
    
    print(f"Found {len(uniq)} for {domain_name}")
    all_data.extend(uniq[:50])

with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Domain", "Company", "Role", "Location", "Is Remote", "URL", "Description"])
    writer.writeheader()
    writer.writerows(all_data)

print(f"Done. Wrote {len(all_data)} jobs to {output_file}")
