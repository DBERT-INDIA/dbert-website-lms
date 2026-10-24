import os
import csv
import datetime
from datetime import timedelta
from playwright.sync_api import sync_playwright
import time
import sys

# To fix windows console unicode printing issues if any
sys.stdout.reconfigure(encoding='utf-8')

DOMAINS = {
    "AI Agent Development": [
        "artificial-intelligence-ai-internship", 
        "machine-learning-internship",
        "deep-learning-internship"
    ],
    "Data Analyst": [
        "data-science-internship", 
        "data-analytics-internship", 
        "business-analytics-internship"
    ],
    "Full Stack Development": [
        "full-stack-development-internship", 
        "web-development-internship", 
        "backend-development-internship", 
        "front-end-development-internship"
    ],
    "Python Automation": [
        "python-internship", 
        "software-testing-internship"
    ]
}

CSV_FILE = 'indian_master_internships.csv'

def setup_csv():
    headers = ['Domain', 'Company', 'Role', 'Location', 'Is Remote', 'Start Date', 'End Date / Duration', 'Stipend / Salary', 'URL', 'Description']
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

def append_to_csv(data):
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def is_remote(location):
    if location and ('work from home' in location.lower() or 'remote' in location.lower()):
        return 'Yes'
    return 'No'

def scrape_internshala():
    setup_csv()
    total_count = 0
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    end_date_str = (datetime.datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        page = context.new_page()
        
        for domain, categories in DOMAINS.items():
            for category in categories:
                page_num = 1
                while total_count < 1400:
                    url = f"https://internshala.com/internships/{category}/page-{page_num}/"
                    print(f"Loading {url}")
                    try:
                        page.goto(url, timeout=30000)
                        page.wait_for_selector('.internship_meta, .error_text', timeout=10000)
                    except Exception as e:
                        print(f"Error loading page: {e}")
                        break
                    
                    cards = page.locator('.internship_meta')
                    count = cards.count()
                    print(f"Found {count} cards on page {page_num}")
                    
                    if count == 0:
                        break # no more internships on this category
                        
                    for i in range(count):
                        if total_count >= 1400: break
                        try:
                            card = cards.nth(i)
                            
                            title_el = card.locator('.job-title-href')
                            title = title_el.inner_text().strip() if title_el.count() > 0 else ""
                            link = title_el.get_attribute('href') if title_el.count() > 0 else ""
                            if link and not link.startswith('http'):
                                link = "https://internshala.com" + link
                                
                            company_el = card.locator('.company-name')
                            company = company_el.inner_text().strip() if company_el.count() > 0 else ""
                            
                            loc_el = card.locator('.locations')
                            location = loc_el.inner_text().strip() if loc_el.count() > 0 else ""
                            remote_flag = is_remote(location)
                            
                            items = card.locator('.item_body')
                            duration = items.nth(1).inner_text().strip() if items.count() > 1 else ""
                            if not duration: duration = end_date_str
                            
                            stipend_el = card.locator('.stipend')
                            stipend = stipend_el.inner_text().strip() if stipend_el.count() > 0 else "Not Disclosed"
                            
                            description = f"Internshala Listing: {title} at {company}."
                            
                            if title and company:
                                append_to_csv([domain, company, title, location, remote_flag, today, duration, stipend, link, description])
                                total_count += 1
                        except Exception as inner_e:
                            print(f"Error parsing card: {inner_e}")
                            continue
                    
                    page_num += 1
                    time.sleep(1.5) # Be polite
        browser.close()
    return total_count

if __name__ == "__main__":
    c = scrape_internshala()
    print(f"Scraping complete! Total extracted: {c}")
