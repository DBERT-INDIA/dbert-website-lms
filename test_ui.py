import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://127.0.0.1:5000/admin-login')
        page.fill('input[name="email"]', 'dbert_superadmin')
        page.fill('input[name="password"]', 'dbert123')
        page.click('button[type="submit"]')
        time.sleep(1)
        
        page.on('console', lambda msg: print(f'CONSOLE {msg.type}: {msg.text}'))
        page.on('pageerror', lambda exc: print(f'PAGE ERROR: {exc}'))
        
        page.goto('http://127.0.0.1:5000/admin/sourcing-dashboard')
        time.sleep(2)
        
        print('Total KPI text:', page.locator('#kpi-total').inner_text())
        browser.close()
run()
