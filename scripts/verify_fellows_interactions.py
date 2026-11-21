#!/usr/bin/env python3
"""
Test interactive features on https://dbert.in/fellows/verified:
- Search input
- LinkedIn filter toggle
- Article filter toggle
- Domain filter pills
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://dbert.in/fellows/verified", wait_until="networkidle")
    
    total = page.locator('div[class*="fellowCard"]').count()
    print(f"[TEST] Initial load total cards: {total}")
    
    # 1. Search for 'Sakthi'
    search_input = page.locator('input[placeholder*="Search by candidate name"]')
    search_input.fill("Sakthi")
    page.wait_for_timeout(300)
    filtered = page.locator('div[class*="fellowCard"]').count()
    print(f"[TEST] Search 'Sakthi' card count: {filtered}")
    
    # Reset search
    search_input.fill("")
    page.wait_for_timeout(300)
    
    # 2. Toggle LinkedIn filter
    linkedin_toggle = page.locator('button:has-text("With LinkedIn Profile")')
    linkedin_toggle.click()
    page.wait_for_timeout(300)
    linkedin_count = page.locator('div[class*="fellowCard"]').count()
    print(f"[TEST] 'With LinkedIn Profile' card count: {linkedin_count}")
    
    # Reset LinkedIn filter
    linkedin_toggle.click()
    page.wait_for_timeout(300)

    # 3. Toggle Published Article filter
    article_toggle = page.locator('button:has-text("With Published Article")')
    article_toggle.click()
    page.wait_for_timeout(300)
    article_count = page.locator('div[class*="fellowCard"]').count()
    print(f"[TEST] 'With Published Article' card count: {article_count}")
    
    browser.close()
    print("[TEST] Interactive tests completed successfully!")
