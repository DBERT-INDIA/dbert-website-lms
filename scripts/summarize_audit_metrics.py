import json

with open('data/audit_portal_48h.json', encoding='utf-8') as f:
    d = json.load(f)

print('--- AUDIT METRICS SUMMARY ---')
print('Generated At:', d['report_meta']['generated_at'])
print('Window:', d['report_meta']['window_48h_since'])

print('\n=== 1. OVERALL APPLICATIONS DATABASE (4,931 Total Records) ===')
for s in d['app_statuses']:
    print(f"  * {s['status']}: {s['count']}")

print(f"\n=== 2. RECENT APPLICATIONS IN 48H WINDOW ({len(d['recent_apps_48h'])} Records) ===")
recent_app_statuses = {}
for a in d['recent_apps_48h']:
    recent_app_statuses[a['status']] = recent_app_statuses.get(a['status'], 0) + 1
for st, cnt in recent_app_statuses.items():
    print(f"  * {st}: {cnt}")

print(f"\n=== 3. SESSIONS & USERS LOGGED IN (LAST 48H) ===")
print('Unique Users Logged In:', d['unique_users_48h_count'])
print('Role Breakdown:')
for role, cnt in d['by_role_48h'].items():
    print(f"  * Role '{role}': {cnt}")

users = d['users_detail_48h']
user_app_st = {}
user_enr_st = {}
g1_cnt = 0
g2_pub_cnt = 0
g2_rev_cnt = 0
g2_draft_cnt = 0
g3_cnt = 0
g4_cnt = 0
stipend_ready_cnt = 0

for u in users:
    ast = u['app_status']
    est = u['enr_status']
    user_app_st[ast] = user_app_st.get(ast, 0) + 1
    user_enr_st[est] = user_enr_st.get(est, 0) + 1
    if u['g1_linkedin']: g1_cnt += 1
    art_st = str(u['g2_article_status']).upper()
    if art_st == 'PUBLISHED': g2_pub_cnt += 1
    elif 'REVIEW' in art_st: g2_rev_cnt += 1
    elif 'DRAFT' in art_st: g2_draft_cnt += 1
    if u['g3_verified']: g3_cnt += 1
    if u['g4_github']: g4_cnt += 1
    if u['stipend_ready']: stipend_ready_cnt += 1

print('\n=== 4. ACTIVE USERS (220) — APPLICATION STATUS BREAKDOWN ===')
for k, v in user_app_st.items():
    print(f"  * {k}: {v} ({v/len(users)*100:.1f}%)")

print('\n=== 5. ACTIVE USERS (220) — ENROLLMENT STATUS BREAKDOWN ===')
for k, v in user_enr_st.items():
    print(f"  * {k}: {v} ({v/len(users)*100:.1f}%)")

print('\n=== 6. ACTIVE USERS (220) — 4-STEP STIPEND PROGRESSION GATES ===')
print(f"  * Gate 1 (LinkedIn Profile Connected): {g1_cnt} / {len(users)} ({g1_cnt/len(users)*100:.1f}%)")
print(f"  * Gate 2 (Technical Case Study): Published={g2_pub_cnt}, In Review={g2_rev_cnt}, Draft={g2_draft_cnt}, None={len(users)-g2_pub_cnt-g2_rev_cnt-g2_draft_cnt}")
print(f"  * Gate 3 (₹299 Credential Verification): {g3_cnt} / {len(users)} ({g3_cnt/len(users)*100:.1f}%)")
print(f"  * Gate 4 (Active GitHub Repository): {g4_cnt} / {len(users)} ({g4_cnt/len(users)*100:.1f}%)")
print(f"  * All 4 Gates Completed (Stipend Release Ready): {stipend_ready_cnt}")

print('\n=== 7. GLOBAL DATABASE TOTALS (ACROSS ALL 405/472 ENROLLED INTERNS) ===')
print('  * Total Intern Accounts:', d['global_totals']['intern_accounts']['total_accounts'])
print('  * Global Gate 1 (LinkedIn Connected):', d['global_totals']['intern_accounts']['g1_linkedin_count'])
print('  * Global Gate 4 (GitHub Connected):', d['global_totals']['intern_accounts']['g4_github_count'])
print('  * Global Gate 2 (Articles):', d['global_totals']['articles'])
print('  * Global Gate 3 (Certificates):', d['global_totals']['certificates'])
