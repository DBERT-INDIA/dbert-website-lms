import json

d = json.load(open('data/ec2_stipend_submissions_audit.json', encoding='utf-8'))
print(f"Total Submissions: {d['submissions_count']}")
print(f"Cert Columns: {d['cert_cols']}")
approved_orgs = ['alkameinc', 'gayatri-education', 'aivaratechinfomatics', 'dbert-india']

for s in d['submissions']:
    repo = s.get('github_repo_url', '')
    is_org = any(org in repo.lower() for org in approved_orgs) if repo else False
    has_article = bool(s.get('article'))
    print(f"Sub #{s['sub_id']:2d} | Status: {s['sub_status']:17s} | {s['email']:32s} | Org Repo: {str(is_org):5s} | UPI: {str(s['has_upi']):5s} | LinkedIn: {str(s['linkedin_verified']):5s} | Art: {str(has_article):5s} | StipendVer: {str(s['stipend_verified']):5s}")
