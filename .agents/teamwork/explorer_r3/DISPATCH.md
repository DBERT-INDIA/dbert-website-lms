## 2026-10-25T22:49:16Z
[Message] timestamp=2026-10-25T22:49:16Z sender=3a4d7ac2-699c-47ca-9101-c0e51547ba94 priority=MESSAGE_PRIORITY_HIGH content=You are explorer_r3 (Role: Website Readiness Auditor).
Your working directory is: c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_r3
The project workspace root is: c:\Users\user\Desktop\dbert-website-lms
You MUST read: c:\Users\user\Desktop\dbert-website-lms\ORIGINAL_REQUEST.md

Your task is requirement R3 from ORIGINAL_REQUEST.md:
Audit `cpanel_public_html/` (the deployed static build) and `apps/website/` source:
1. Dead internal links: Enumerate every `href` in every HTML file pointing to `/something` — check whether that path exists as a directory with index.html in cpanel_public_html/. Produce a complete table of (href -> target exists? yes/no) and list all 404 dead ends.
2. Missing or broken 404 page: Verify cpanel_public_html/404.html or cpanel_public_html/404/index.html exists; check Nginx config has error_page 404 directive.
3. sitemap.xml domain check: Every <loc> entry must be https://dbert.in/...
4. robots.txt check: Sitemap: directive must point to https://dbert.in/sitemap.xml.
5. OG / meta tags across all pages: og:url, og:image, twitter:site must use dbert.in.
6. _next/ asset integrity: Sample-check that JS/CSS src and href paths referenced in HTML files (/_next/static/chunks/...) actually exist in cpanel_public_html/_next/static/.
7. JSON-LD structured data: Any Organization, WebSite, BreadcrumbList schema markup must use dbert.in URLs. Check all pages with this issue.

Requirements for output:
For EVERY finding, cite the exact relative file path and line number, classification (Blocker/Warning/Info), explanation, and recommended fix. Include the complete Dead Internal Links table.
Write your complete, self-contained report to:
c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_r3\handoff.md
Update c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_r3\progress.md as you work.
When done, notify orchestrator via send_message with a brief summary and path to your handoff.md.
