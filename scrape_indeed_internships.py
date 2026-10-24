import os
import csv
import datetime
from datetime import timedelta
from playwright.sync_api import sync_playwright
import time
import re

DOMAINS = {
    "AI Agent Development": ["artificial+intelligence+internship", "machine+learning+internship", "generative+ai+internship"],
    "Data Analyst": ["data+analyst+internship", "data+science+internship"],
    "Full Stack Development": ["full+stack+internship", "web+development+internship"],
    "Python Automation": ["python+internship", "rpa+internship", "automation+internship"]
}

CSV_FILE = 'indian_master_internships.csv'

def append_to_csv(data):
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def is_remote(location):
    if location and ('remote' in location.lower() or 'home' in location.lower()):
        return 'Yes'
    return 'No'

def scrape_indeed():
    total_count = 0
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    end_date_str = (datetime.datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        page = context.new_page()
        
        for domain, keywords in DOMAINS.items():
            for keyword in keywords:
                start = 0
                max_pages = 2 # Scrape 2 pages per keyword to not push indeed too hard
                
                for page_num in range(max_pages):
                    url = f"https://in.indeed.com/jobs?q={keyword}&l=India&start={start}"
                    print(f"Loading {url}")
                    try:
                        page.goto(url, timeout=30000)
                        page.wait_for_timeout(3000) # Give Indeed time to render
                    except Exception as e:
                        print(f"Error loading Indeed: {e}")
                        break
                    
                    cards = page.locator('.job_seen_beacon')
                    count = cards.count()
                    print(f"Found {count} cards for {keyword} on Indeed")
                    
                    if count == 0:
                        break
                        
                    for i in range(count):
                        try:
                            card = cards.nth(i)
                            
                            title_el = card.locator('h2.jobTitle span[title]')
                            if title_el.count() == 0:
                                title_el = card.locator('h2.jobTitle span')
                            title = title_el.first.inner_text().strip() if title_el.count() > 0 else ""
                            
                            link_el = card.locator('h2.jobTitle a')
                            link = link_el.get_attribute('href') if link_el.count() > 0 else ""
                            if link and not link.startswith('http'):
                                link = "https://in.indeed.com" + link
                                
                            company_el = card.locator('[data-testid="company-name"]')
                            company = company_el.inner_text().strip() if company_el.count() > 0 else "Unknown"
                            
                            loc_el = card.locator('[data-testid="text-location"]')
                            location = loc_el.inner_text().strip() if loc_el.count() > 0 else "India"
                            remote_flag = is_remote(location)
                            
                            stipend_el = card.locator('.salary-snippet-container')
                            stipend = stipend_el.inner_text().strip() if stipend_el.count() > 0 else "Not Disclosed"
                            
                            description = f"Indeed Listing: {title} at {company}. Apply at URL."
                            
                            if title and company:
                                append_to_csv([domain, company, title, location, remote_flag, today, end_date_str, stipend, link, description])
                                total_count += 1
                        except Exception as inner_e:
                            print(f"Error parsing Indeed card: {inner_e}")
                            continue
                    
                    start += 10
        browser.close()
    return total_count

if __name__ == "__main__":
    print("Starting Indeed Scraping...")
    c = scrape_indeed()
    print(f"Indeed Scraping complete! Total appended: {c}")
