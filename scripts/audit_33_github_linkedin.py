import subprocess
import json
import os
import re
from urllib.parse import urlparse

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
SERVER = "ubuntu@3.26.237.171"
OUTPUT_REPORT = "data/github_linkedin_audit_report.json"

OFFICIAL_ORGS = [
    "alkameinc",
    "ainabhinavsharma",
    "gayatri-education",
    "dbert-india",
    "aivara-technologies",
    "aivaratechinfomatics"
]

OFFICIAL_REPOS = [
    "alkame-nifty-50-educational",
    "gayatri-demo",
    "gayatri-ai",
    "gayatri-tutor-v3",
    "gayatribot-hr",
    "dbert-agent",
    "aivara-insight-lite",
    "internshipportal"
]

def classify_github_url(url):
    if not url or not isinstance(url, str):
        return "INVALID_URL", "No GitHub URL provided"
    
    url = url.strip()
    if not ("github.com" in url.lower()):
        return "INVALID_URL", f"Not a GitHub URL: {url}"
    
    # Clean URL
    clean = url.rstrip("/").replace(".git", "")
    
    # Check for Pull Request: github.com/{org}/{repo}/pull/{id}
    pr_match = re.search(r"github\.com/([^/]+)/([^/]+)/pull/(\d+)", clean, re.IGNORECASE)
    if pr_match:
        org = pr_match.group(1).lower()
        repo = pr_match.group(2).lower()
        pr_id = pr_match.group(3)
        
        is_official_org = org in OFFICIAL_ORGS
        is_official_repo = any(r in repo for r in OFFICIAL_REPOS)
        
        if is_official_org or is_official_repo:
            return "PR_PASSED", f"Valid upstream PR #{pr_id} on {org}/{repo}"
        else:
            return "PR_UNOFFICIAL_REPO", f"PR #{pr_id} on non-official repository: {org}/{repo}"
    
    # Check if repository URL
    repo_match = re.search(r"github\.com/([^/]+)/([^/]+)", clean, re.IGNORECASE)
    if repo_match:
        owner = repo_match.group(1).lower()
        repo = repo_match.group(2).lower()
        
        is_official_org = owner in OFFICIAL_ORGS
        is_official_repo = any(r in repo for r in OFFICIAL_REPOS)
        
        if is_official_org:
            return "BASE_REPO_NO_PR", f"Submitted base organization repository ({owner}/{repo}) without an individual Pull Request"
        elif is_official_repo:
            return "FORK_NO_PR", f"Personal fork of official repo ({owner}/{repo}) without an upstream Pull Request"
        else:
            return "UNOFFICIAL_REPO", f"Standalone personal repository ({owner}/{repo}) not on our 4 project repos"
            
    return "INVALID_URL", f"Unrecognized GitHub URL format: {url}"

def classify_linkedin_url(url, verified_flag):
    if not url or not isinstance(url, str):
        return "LI_MISSING", "No LinkedIn URL provided"
    
    url = url.strip()
    if not ("linkedin.com" in url.lower()):
        return "LI_INVALID", f"Not a LinkedIn URL: {url}"
    
    handle_match = re.search(r"linkedin\.com/(?:in|posts)/([^/?#]+)", url, re.IGNORECASE)
    if not handle_match:
        return "LI_INVALID", f"Invalid LinkedIn profile or post URL structure: {url}"
    
    handle = handle_match.group(1)
    
    if verified_flag == 1 or verified_flag is True:
        return "LI_PASSED", f"Valid LinkedIn profile (in/{handle}) with DBERT credential verified"
    else:
        return "LI_PENDING_CERT", f"Valid LinkedIn profile (in/{handle}), but DBERT credential not yet verified under Licenses & Certifications"

# Remote extraction script
remote_py = r'''
import sys
import json
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

with get_db() as conn:
    # 1. Fetch all submissions for stipend milestone
    cur = conn.execute("""
        SELECT s.id as sub_id, s.intern_id, s.status as sub_status, s.github_repo_url, s.live_demo_url, 
               s.report_file_url, s.ai_evaluation_notes, s.created_at,
               a.name, a.email, a.domain, a.linkedin_url, a.github_url as acct_github,
               a.linkedin_verified, a.stipend_verified, a.stipend_release_date,
               c.cert_id
        FROM task_submissions s
        JOIN tasks t ON t.id = s.task_id
        JOIN intern_accounts a ON a.id = s.intern_id
        LEFT JOIN intern_certificates c ON c.intern_id = a.id OR LOWER(c.email) = LOWER(a.email)
        WHERE (t.task_type = 'stipend_milestone' OR s.task_category = 'stipend_milestone')
        ORDER BY s.id DESC
    """)
    submissions = [dict(r) for r in cur.fetchall()]
    
    # 2. Fetch all verified candidate accounts (Tier 2)
    cur_v = conn.execute("""
        SELECT DISTINCT a.id, a.name, a.email, a.domain, a.stipend_verified, a.stipend_release_date, 
               a.upi_id_encrypted, a.linkedin_url, a.linkedin_verified, a.github_url as acct_github,
               c.cert_id, c.tier
        FROM intern_accounts a
        LEFT JOIN intern_certificates c ON c.intern_id = a.id OR LOWER(c.email) = LOWER(a.email)
        WHERE c.tier = 'verified' OR a.stipend_verified = 1
        ORDER BY a.id ASC
    """)
    verified_accounts = [dict(r) for r in cur_v.fetchall()]
    
    print("PAYLOAD_START")
    print(json.dumps({"submissions": submissions, "verified_accounts": verified_accounts}))
    print("PAYLOAD_END")
'''

print("Fetching live database records from EC2 PostgreSQL...")
res = subprocess.run(
    ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", SERVER, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3"],
    input=remote_py,
    text=True,
    capture_output=True,
    encoding="utf-8"
)

out = res.stdout
if "PAYLOAD_START" not in out:
    print("Failed to fetch payload. Stderr:", res.stderr)
    print("Stdout:", out)
    exit(1)

raw_data = json.loads(out.split("PAYLOAD_START")[1].split("PAYLOAD_END")[0].strip())
submissions_raw = raw_data["submissions"]
verified_raw = raw_data["verified_accounts"]

print(f"Extracted {len(submissions_raw)} submission records and {len(verified_raw)} verified account records.")

# Deduplicate submissions by intern_id (keep latest)
latest_subs = {}
for s in submissions_raw:
    iid = s["intern_id"]
    if iid not in latest_subs:
        latest_subs[iid] = s

print(f"Unique candidate submissions in queue: {len(latest_subs)}")

# Audit Tier 1: 33 Submissions (28 unique candidates)
audited_submissions = []
pr_passed_count = 0
resubmit_required_count = 0

for iid, s in latest_subs.items():
    gh_url = s.get("github_repo_url") or s.get("acct_github") or ""
    li_url = s.get("linkedin_url") or ""
    li_flag = s.get("linkedin_verified")
    
    gh_verdict, gh_reason = classify_github_url(gh_url)
    li_verdict, li_reason = classify_linkedin_url(li_url, li_flag)
    
    overall_pass = (gh_verdict == "PR_PASSED") and (li_verdict == "LI_PASSED")
    
    reasons = []
    if gh_verdict != "PR_PASSED":
        reasons.append(f"GitHub: {gh_reason}")
    if li_verdict != "LI_PASSED":
        reasons.append(f"LinkedIn: {li_reason}")
        
    structured_feedback = (
        "Action Required - Revision Requested:\n"
        "1. GitHub Deliverable: All stipend capstone deliverables must be submitted as an active Pull Request (PR) URL "
        "against one of DBERT's 4 official project repositories: Alkameinc/alkame-nifty-50-educational, "
        "Gayatri-Education/Gayatri-Demo, DBERT-INDIA/dbert-agent, or DBERT-INDIA/Internshipportal. "
        f"Your current submission ({gh_url}) was flagged: {gh_reason}. Please open a PR against upstream and submit the PR URL.\n"
        "2. LinkedIn Credential: You must add DBERT to your LinkedIn profile under 'Licenses & Certifications'. "
        f"Status: {li_reason}. Use your 1-Click certification launcher on /stipend/tasks or link your public credential."
    )
    
    if overall_pass:
        pr_passed_count += 1
        decision = "APPROVED_READY"
    else:
        resubmit_required_count += 1
        decision = "CHANGES_REQUESTED"
        
    audited_submissions.append({
        "sub_id": s["sub_id"],
        "intern_id": iid,
        "name": s["name"],
        "email": s["email"],
        "domain": s["domain"],
        "cert_id": s.get("cert_id"),
        "current_status": s["sub_status"],
        "submitted_github": gh_url,
        "github_verdict": gh_verdict,
        "github_reason": gh_reason,
        "account_linkedin": li_url,
        "linkedin_verdict": li_verdict,
        "linkedin_reason": li_reason,
        "decision": decision,
        "structured_feedback": structured_feedback if decision == "CHANGES_REQUESTED" else "Meets deliverable requirements."
    })

# Audit Tier 2: All Verified Interns Cohort
tier2_audited = []
seen_v_emails = set()
for a in verified_raw:
    em = (a["email"] or "").strip().lower()
    if em in seen_v_emails:
        continue
    seen_v_emails.add(em)
    
    acct_gh = a.get("acct_github") or ""
    acct_li = a.get("linkedin_url") or ""
    li_flag = a.get("linkedin_verified")
    
    gh_v, gh_r = classify_github_url(acct_gh)
    li_v, li_r = classify_linkedin_url(acct_li, li_flag)
    
    has_sub = a["id"] in latest_subs
    sub_info = latest_subs.get(a["id"])
    
    tier2_audited.append({
        "intern_id": a["id"],
        "name": a["name"],
        "email": a["email"],
        "domain": a["domain"],
        "cert_id": a.get("cert_id"),
        "stipend_release_date": a.get("stipend_release_date") or "2026-12-03",
        "has_upi": bool(a.get("upi_id_encrypted")),
        "has_submission": has_sub,
        "sub_status": sub_info["sub_status"] if sub_info else "NOT_SUBMITTED",
        "account_github": acct_gh,
        "github_verdict": gh_v,
        "account_linkedin": acct_li,
        "linkedin_verdict": li_v
    })

report_data = {
    "summary": {
        "tier1_total_submissions": len(submissions_raw),
        "tier1_unique_candidates": len(latest_subs),
        "tier1_pr_passed": pr_passed_count,
        "tier1_resubmit_required": resubmit_required_count,
        "tier2_total_verified_candidates": len(tier2_audited),
        "tier2_has_submission": sum(1 for a in tier2_audited if a["has_submission"]),
        "tier2_missing_submission": sum(1 for a in tier2_audited if not a["has_submission"]),
        "tier2_missing_upi": sum(1 for a in tier2_audited if not a["has_upi"]),
        "tier2_missing_linkedin_cert": sum(1 for a in tier2_audited if a["linkedin_verdict"] != "LI_PASSED")
    },
    "tier1_submissions": audited_submissions,
    "tier2_verified_cohort": tier2_audited
}

os.makedirs("data", exist_ok=True)
with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
    json.dump(report_data, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 80)
print("AUDIT COMPLETE")
print("=" * 80)
print(f"Tier 1 (Submissions in Review): {len(latest_subs)} unique candidates")
print(f"  • PR & LinkedIn PASSED (Approved Ready): {pr_passed_count}")
print(f"  • Resubmission Required (Changes Requested): {resubmit_required_count}")
print(f"Tier 2 (Verified Cohort for 03 Dec Release): {len(tier2_audited)} unique candidates")
print(f"  • Submitted Capstone Dossier: {report_data['summary']['tier2_has_submission']}")
print(f"  • Missing Capstone Dossier: {report_data['summary']['tier2_missing_submission']}")
print(f"  • Missing Encrypted UPI: {report_data['summary']['tier2_missing_upi']}")
print(f"Full report saved to: {OUTPUT_REPORT}")
