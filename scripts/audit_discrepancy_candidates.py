import sys
import json
from pathlib import Path

if Path("/var/www/dbert-website-lms").exists():
    sys.path.insert(0, "/var/www/dbert-website-lms/apps/portal")
else:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "apps" / "portal"))

from app import get_db

conn = get_db()
cur = conn.cursor()

APPROVED_ORGS = [
    "gayatri-education",
    "aivaratechinfomatics",
    "alkameinc",
    "dbert-india"
]

print("=" * 80)
print("AUDITING USERS WITH INVALID GITHUB CONTRIBUTIONS OR UNVERIFIED LINKEDIN")
print("=" * 80)

# 1. Check all task_submissions for stipend_milestone
cur.execute("""
    SELECT ts.id, ts.intern_id, ts.email, ts.github_repo_url, ts.status,
           ia.name, ia.linkedin_url, ia.linkedin_verified, ia.linkedin_verification_status,
           ia.stipend_verified, ia.upi_id_encrypted
    FROM task_submissions ts
    JOIN intern_accounts ia ON ts.intern_id = ia.id
    WHERE ts.task_category = 'stipend_milestone'
    ORDER BY ts.id DESC
""")
subs = cur.fetchall()
print(f"Total stipend milestone submissions: {len(subs)}")

invalid_github_subs = []
unverified_linkedin_subs = []

for s in subs:
    sid, iid, em, gh_url, s_status, name, l_url, l_ver, l_status, st_ver, upi = s
    gh_lower = (gh_url or "").lower()
    
    # Check if gh_url belongs to any approved org
    is_approved_org = any(org in gh_lower for org in APPROVED_ORGS)
    
    # Check if candidate has stipend_verified == 1 (already verified Cohort D)
    if st_ver == 1:
        continue
        
    has_gh = bool(gh_lower.strip())
    has_li = bool(l_url and str(l_url).strip())
    is_li_verified = bool(l_ver == 1)

    issue = {}
    if has_gh and not is_approved_org:
        issue["github_issue"] = f"GitHub URL '{gh_url}' does not belong to an approved DBERT organization ({', '.join(APPROVED_ORGS)})."
    if has_li and not is_li_verified:
        issue["linkedin_issue"] = f"LinkedIn profile '{l_url}' is not verified / experience not detected (status: {l_status or 'UNVERIFIED'})."
    
    if issue:
        issue.update({
            "submission_id": sid,
            "intern_id": iid,
            "name": name or "Fellow",
            "email": em,
            "github_repo_url": gh_url,
            "linkedin_url": l_url,
            "linkedin_status": l_status,
            "has_upi": bool(upi and str(upi).strip())
        })
        invalid_github_subs.append(issue)

print(f"\nStipend submission candidates with issues (Invalid GitHub or Unverified LinkedIn): {len(invalid_github_subs)}")
for item in invalid_github_subs:
    print(f"  * {item['name']} <{item['email']}>")
    if "github_issue" in item:
        print(f"    - {item['github_issue']}")
    if "linkedin_issue" in item:
        print(f"    - {item['linkedin_issue']}")

# 2. Check broader intern_accounts who have submitted github_url in profile, but not approved org
cur.execute("""
    SELECT id, name, email, github_url, linkedin_url, linkedin_verified, linkedin_verification_status, upi_id_encrypted, stipend_verified
    FROM intern_accounts
    WHERE (github_url IS NOT NULL AND github_url != '')
      AND (stipend_verified IS NULL OR stipend_verified = 0)
""")
accts_with_gh = cur.fetchall()
print(f"\nIntern accounts with GitHub URL configured: {len(accts_with_gh)}")

unrelated_gh_accounts = []
for a in accts_with_gh:
    aid, aname, aemail, agh, ali, aliver, alistatus, aupi, astipend = a
    agh_lower = (agh or "").lower()
    is_approved = any(org in agh_lower for org in APPROVED_ORGS)
    if not is_approved:
        unrelated_gh_accounts.append({
            "intern_id": aid,
            "name": aname or "Fellow",
            "email": aemail,
            "github_url": agh,
            "linkedin_url": ali,
            "linkedin_verified": aliver,
            "has_upi": bool(aupi and str(aupi).strip())
        })

print(f"Intern accounts with unrelated GitHub URLs (not under approved orgs): {len(unrelated_gh_accounts)}")
print(f"Sample 5 unrelated GitHub accounts:")
for u in unrelated_gh_accounts[:5]:
    print(f"  * {u['name']} <{u['email']}> -> {u['github_url']}")

# 3. Check intern accounts with LinkedIn URL configured but unverified
cur.execute("""
    SELECT count(*) FROM intern_accounts
    WHERE (linkedin_url IS NOT NULL AND linkedin_url != '')
      AND (linkedin_verified IS NULL OR linkedin_verified = 0)
      AND (stipend_verified IS NULL OR stipend_verified = 0)
""")
unverified_li_count = cur.fetchone()[0]
print(f"\nIntern accounts with unverified LinkedIn profile: {unverified_li_count}")
