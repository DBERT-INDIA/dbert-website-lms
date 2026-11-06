import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("Navigating to https://dbert.in/eroll?email=bhargavi13032007@gmail.com ...")
        await page.goto("https://dbert.in/eroll?email=bhargavi13032007@gmail.com", timeout=30000)
        
        # Wait for the approved title to appear
        print("Waiting for approved title...")
        approved_el = await page.wait_for_selector("text=OFFICIAL ENROLLMENT APPROVED & SEAT CONFIRMED", timeout=15000)
        
        url = page.url
        print(f"Current URL: {url}")
        
        title_text = await page.locator("h1").inner_text()
        print(f"Title: {title_text}")
        
        # Check countdown text
        countdown_tiles = await page.locator("[class*='countdownTile']").all_inner_texts()
        print(f"Countdown Tiles: {countdown_tiles}")
        
        # Check kickoff text
        kickoff = await page.locator("[class*='countdownKickoffDate']").inner_text()
        print(f"Kickoff info: {kickoff}")
        
        # Check candidate details
        candidate_name = await page.locator("text=Bhargavi Poola").first.inner_text()
        print(f"Candidate element found: {candidate_name}")
        
        # Check UTR
        utr_elem = await page.locator("text=679862090077").first.inner_text()
        print(f"UTR element found: {utr_elem}")
        
        # Take a screenshot
        screenshot_path = "outputs/bhargavi_approved_live.png"
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"Saved screenshot to {screenshot_path}")
        
        await browser.close()

asyncio.run(main())
