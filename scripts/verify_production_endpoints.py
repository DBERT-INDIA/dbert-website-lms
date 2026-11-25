import urllib.request
import json
import ssl
import sys

print("=" * 80)
print("LIVE PRODUCTION VERIFICATION FOR DBERT.IN & LMS.DBERT.IN")
print("=" * 80)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def check_url(url, expected_snippets=None, min_status=200, max_status=200):
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) DBERT-Verification/2.0'}
        )
        with urllib.request.urlopen(req, timeout=20, context=ctx) as response:
            status = response.status
            body = response.read().decode('utf-8', errors='replace')
            if not (min_status <= status <= max_status):
                print(f"❌ FAIL: {url} returned status {status}")
                return False
            if expected_snippets:
                for snippet in expected_snippets:
                    if snippet not in body:
                        print(f"❌ FAIL: {url} missing expected snippet '{snippet}'")
                        return False
            print(f"✅ PASS [HTTP {status}]: {url}")
            return True
    except Exception as e:
        print(f"💥 ERROR: {url} -> {e}")
        return False

tests = [
    # 1. Sitemaps
    ("https://dbert.in/sitemap.xml", [
        "<?xml", 
        "https://dbert.in/courses/ai-agent-development", 
        "https://dbert.in/verify/directory/cybersecurity", 
        "https://dbert.in/internships/full-stack-development/bengaluru"
    ]),
    ("https://lms.dbert.in/sitemap.xml", ["<?xml", "https://lms.dbert.in/"]),

    # 2. Dynamic Course Pages (All 9 Domains)
    ("https://dbert.in/courses/ai-agent-development", [
        "AI Agent &amp; Multi-Agent Systems Engineering", 
        "Structure 1: Fellowship", 
        "Structure 2: Paid Course"
    ]),
    ("https://dbert.in/courses/full-stack-development", [
        "Full Stack Web &amp; AI Systems Engineering", 
        "Next.js 16", 
        "2-Month Fellowship"
    ]),
    ("https://dbert.in/courses/data-analytics", ["Data Analytics &amp; Automated Corporate BI", "Power BI", "SQL"]),
    ("https://dbert.in/courses/cybersecurity", ["Cybersecurity &amp; Threat Defense Engineering", "OWASP Top 10", "Burp Suite"]),
    ("https://dbert.in/courses/devops-cloud", ["DevOps &amp; Cloud Systems Engineering", "Docker", "Kubernetes", "AWS"]),
    ("https://dbert.in/courses/mobile-app-development", ["Mobile App Development (Flutter &amp; React Native)", "Flutter", "SQLite"]),
    ("https://dbert.in/courses/python-automation", ["Python Automation &amp; Web Extraction Engineering", "Playwright", "Celery"]),
    ("https://dbert.in/courses/ui-ux-design", ["UI/UX Design &amp; Venture Product Prototyping", "Figma", "Auto-Layout"]),
    ("https://dbert.in/courses/generative-ai", ["Generative AI &amp; LLM Systems Engineering", "LoRA / QLoRA", "PyTorch"]),

    # 3. Dynamic Single-Segment Internship Pages
    ("https://dbert.in/internships/bengaluru", ["Software &amp; AI Internships in Bengaluru", "Manyata Tech Park", "Bengaluru"]),
    ("https://dbert.in/internships/ai-agent-development", ["AI Agent &amp; LLM Systems Internships", "LangGraph", "5,000"]),
    ("https://dbert.in/internships/full-stack-development/bengaluru", ["Full Stack Web Development Intern (Bengaluru)", "Outer Ring Road", "5000"]),

    # 4. Canonical Domain Directories
    ("https://dbert.in/verify/directory/cybersecurity", ["Pre-Vetted Cybersecurity Engineers", "OWASP Top 10"]),
    ("https://dbert.in/verify/directory/ai-agent-development", ["Pre-Vetted AI Agent Developers", "LangGraph"]),

    # 5. Core Incubation & Verification Gates
    ("https://dbert.in/enroll/1999", ["1,999", "Technical Incubation Enrollment"]),
    ("https://dbert.in/verify/directory", ["Pre-Vetted Software &amp; AI Engineers"]),
    ("https://dbert.in/dbert-online", ["dbert.in"])
]

all_passed = True
for url, snippets in tests:
    if not check_url(url, snippets):
        all_passed = False

# 6. Test Live Lead Capture API
print("\n[TEST] Testing live POST /api/leads/capture on dbert.in...")
try:
    lead_payload = {
        "name": "Production Verification Robot",
        "email": "telemetry-verify@dbert.in",
        "phone": "9999988888",
        "college": "IIT Delhi",
        "domain": "ai-agent-development",
        "programInterest": "fellowship",
        "city": "Bengaluru"
    }
    lead_req = urllib.request.Request(
        "https://dbert.in/api/leads/capture",
        data=json.dumps(lead_payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "DBERT-LiveVerify/2.0"}
    )
    with urllib.request.urlopen(lead_req, timeout=15, context=ctx) as lead_res:
        res_body = json.loads(lead_res.read().decode("utf-8"))
        if lead_res.status == 201 and res_body.get("success") is True:
            print(f"✅ PASS [HTTP 201]: Lead capture verified! Lead ID: {res_body.get('leadId')}")
        else:
            print(f"❌ FAIL: Lead capture unexpected response: {res_body}")
            all_passed = False
except Exception as e:
    print(f"💥 ERROR testing lead capture API: {e}")
    all_passed = False

print("=" * 80)
if all_passed:
    print("🎉 ALL 18 PRODUCTION CHECKS & APIS ARE 100% PASSING!")
else:
    print("⚠️ SOME PRODUCTION CHECKS FAILED.")
print("=" * 80)
