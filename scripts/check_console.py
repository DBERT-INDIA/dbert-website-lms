from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context()
    ctx.add_cookies([{
        'name': 'dbert_auth',
        'value': 'b21c99e7fd6143eb63648da7f7d5963fbba699c285ffbbd37b5b0aebcbfcfa1b',
        'domain': 'lms.dbert.in',
        'path': '/'
    }])
    page = ctx.new_page()
    page.on('console', lambda msg: print('CONSOLE:', msg.text))
    page.goto('https://lms.dbert.in/stipend/tasks')
    b.close()
