import sys
import json
import re

sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

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

def classify_github(url):
    if not url or not isinstance(url, str):
        return "MISSING", "No GitHub URL provided", None, None, None
    url = url.strip()
    clean = url.rstrip("/").replace(".git", "")
    if "github.com" not in clean.lower():
        return "INVALID_DOMAIN", f"Not a GitHub domain: {url}", None, None, None
    
    # Check for PR: github.com/{owner}/{repo}/pull/{pr_id}
    pr_match = re.search(r"github\.com/([^/]+)/([^/]+)/pull/(\d+)", clean, re.IGNORECASE)
    if pr_match:
        owner = pr_match.group(1).lower()
        repo = pr_match.group(2).lower()
        pr_id = pr_match.group(3)
        is_official = (owner in OFFICIAL_ORGS) or any(r in repo for r in OFFICIAL_REPOS)
        if is_official:
            return "VALID_UPSTREAM_PR", f"Valid PR #{pr_id} on {owner}/{repo}", owner, repo, pr_id
        else:
            return "PR_ON_UNOFFICIAL_REPO", f"PR #{pr_id} on unofficial repo {owner}/{repo}", owner, repo, pr_id

    # Check if repo: github.com/{owner}/{repo}
    repo_match = re.search(r"github\.com/([^/]+)/([^/]+)", clean, re.IGNORECASE)
    if repo_match:
        owner = repo_match.group(1).lower()
        repo = repo_match.group(2).lower()
        if owner in OFFICIAL_ORGS:
            return "BASE_REPO_NO_PR", f"Base official repo submitted without a PR: {owner}/{repo}", owner, repo, None
        elif any(r in repo for r in OFFICIAL_REPOS):
            return "FORK_NO_PR", f"Personal fork of official repo without an upstream PR: {owner}/{repo}", owner, repo, None
        else:
            return "UNOFFICIAL_REPO", f"Personal standalone repo: {owner}/{repo}", owner, repo, None
            
    return "MALFORMED_URL", f"Malformed GitHub URL: {url}", None, None, None

with get_db() as conn:
    rows = conn.execute("""
        SELECT 
            s.id as sub_id, s.task_id, s.task_category, s.status as sub_status,
            s.github_repo_url, s.live_demo_url, s.report_file_url,
            s.ai_evaluation_score, s.ai_evaluation_status, s.ai_evaluation_notes,
            s.created_at as sub_created_at,
            a.id as intern_id, a.name, a.email, a.phone, a.domain, a.signup_stage,
            a.stipend_verified, a.stipend_release_date, a.stipend_amount,
            (a.upi_id_encrypted IS NOT NULL AND a.upi_id_encrypted != '') as has_upi,
            a.linkedin_url, a.linkedin_verified, a.github_url as acct_github,
            c.cert_id, c.tier as cert_tier
        FROM task_submissions s
        LEFT JOIN intern_accounts a ON a.id = s.intern_id
        LEFT JOIN intern_certificates c ON c.intern_id = a.id
        ORDER BY s.id DESC;
    """).fetchall()

    audit_items = []
    counts_by_status = {}
    counts_by_gh_type = {}
    
    for r in rows:
        d = dict(r)
        gh_type, gh_desc, owner, repo, pr_id = classify_github(d.get("github_repo_url"))
        d["gh_classification"] = gh_type
        d["gh_description"] = gh_desc
        d["gh_owner"] = owner
        d["gh_repo"] = repo
        d["gh_pr_id"] = pr_id
        
        # Cert status
        has_cert = bool(d.get("cert_id"))
        is_verified_cert = bool(d.get("cert_tier") and str(d.get("cert_tier")).lower() == "verified")
        d["has_cert"] = has_cert
        d["is_verified_cert"] = is_verified_cert
        
        audit_items.append(d)
        
        st = d.get("sub_status") or "unknown"
        counts_by_status[st] = counts_by_status.get(st, 0) + 1
        counts_by_gh_type[gh_type] = counts_by_gh_type.get(gh_type, 0) + 1

    summary = {
        "total_submissions": len(audit_items),
        "counts_by_status": counts_by_status,
        "counts_by_gh_type": counts_by_gh_type
    }
    
    out = {
        "summary": summary,
        "submissions": audit_items
    }
    
    with open('/tmp/submissions_93_deep_audit.json', 'w') as f:
        json.dump(out, f, default=str, indent=2)

print("AUDIT_DONE")
print(json.dumps(summary, indent=2))
