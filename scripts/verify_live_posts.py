import urllib.request
import re

urls = [
    'https://lms.dbert.in/jobs/ai-agent-developer-remote-16',
    'https://lms.dbert.in/internships/rag-pipeline-engineering-intern-remote-1'
]

for url in urls:
    print(f"=== Testing: {url} ===")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 DBERT-Test/1.0'})
    with urllib.request.urlopen(req, timeout=15) as res:
        html = res.read().decode('utf-8')
        print("HTTP status:", res.status)
        
        # Check Title tag
        title_match = re.search(r'<title>(.*?)</title>', html)
        print("Title:", title_match.group(1) if title_match else "None")
        
        # Check for 1999 link
        enroll_1999_count = html.count('https://dbert.in/enroll/1999')
        print("Count of dbert.in/enroll/1999 links:", enroll_1999_count)
        
        # Check for Fast-Track text
        has_fast_track = 'Fast-Track Selection Pathway' in html or 'FAST-TRACK SELECTION PATHWAY' in html
        print("Has Fast-Track Pathway text:", has_fast_track)
        
        # Check for Priority Recruiter Shortlisting Available
        has_badge = 'Priority Recruiter Shortlisting Available' in html
        print("Has Priority Recruiter Shortlist Badge:", has_badge)
        
        # Check for Schema.org JSON-LD
        has_jsonld = 'JobPosting' in html
        print("Has Schema.org JobPosting JSON-LD:", has_jsonld)
        print()
