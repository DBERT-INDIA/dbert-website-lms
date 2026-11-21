import os
import sys
from playwright.sync_api import sync_playwright

def generate_pdf():
    # Read the rendered HTML
    with open('janvi_offer_print.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Read portal-offer.css
    css_path = os.path.abspath('apps/portal/static/css/portal-offer.css')
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()

    # Replace relative link with inlined stylesheet and hide the .no-print-bar
    html_content = html_content.replace(
        '<link rel="stylesheet" href="/static/css/portal-offer.css?v=20261115">',
        f'<style>\n{css_content}\n</style>'
    )
    
    # Ensure no-print-bar is removed/hidden for the PDF and print-doc-container is visible
    custom_style = """
    <style>
      .no-print-bar { display: none !important; }
      @page {
        size: A4 portrait;
        margin: 10mm 12mm 10mm 12mm;
      }
      body {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }
      body * {
        visibility: visible !important;
      }
      .print-doc-container, .print-doc-container * {
        visibility: visible !important;
      }
    </style>
    """
    html_content = html_content.replace('</head>', f'{custom_style}\n</head>')
    html_content = html_content.replace('<div class="print-doc-container">', '<div class="print-doc-container" id="printable-offer-letter">')

    # Output directory
    os.makedirs('outputs/offers', exist_ok=True)
    artifact_dir = r'C:\Users\user\.gemini\antigravity\brain\9e76c80f-9681-4f52-a13d-330f08edd6f5'
    os.makedirs(artifact_dir, exist_ok=True)

    local_pdf = os.path.abspath('outputs/offers/DBERT_Offer_Letter_Janvi_Bamane_AIML_5180.pdf')
    artifact_pdf = os.path.join(artifact_dir, 'DBERT_Offer_Letter_Janvi_Bamane_AIML_5180.pdf')

    temp_html_path = os.path.abspath('outputs/offers/janvi_offer_final.html')
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print('Rendering vector PDF via Playwright Chromium...')
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f'file:///{temp_html_path}', wait_until='networkidle')
        # Wait for QR code image to load
        page.wait_for_timeout(2000)
        
        pdf_bytes = page.pdf(
            format='A4',
            print_background=True,
            margin={'top': '10mm', 'bottom': '10mm', 'left': '12mm', 'right': '12mm'}
        )
        browser.close()

    with open(local_pdf, 'wb') as f:
        f.write(pdf_bytes)
    print(f'Saved local PDF: {local_pdf} ({len(pdf_bytes)} bytes)')

    with open(artifact_pdf, 'wb') as f:
        f.write(pdf_bytes)
    print(f'Saved artifact PDF: {artifact_pdf} ({len(pdf_bytes)} bytes)')

if __name__ == '__main__':
    generate_pdf()
