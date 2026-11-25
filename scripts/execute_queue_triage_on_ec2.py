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
        return "MISSING", "No GitHub URL provided"
    url = url.strip()
    clean = url.rstrip("/").replace(".git", "")
    if "github.com" not in clean.lower():
        return "INVALID_DOMAIN", f"Not a GitHub domain: {url}"
    
    # Check for PR: github.com/{owner}/{repo}/pull/{pr_id}
    pr_match = re.search(r"github\.com/([^/]+)/([^/]+)/pull/(\d+)", clean, re.IGNORECASE)
    if pr_match:
        owner = pr_match.group(1).lower()
        repo = pr_match.group(2).lower()
        pr_id = pr_match.group(3)
        is_official = (owner in OFFICIAL_ORGS) or any(r in repo for r in OFFICIAL_REPOS)
        if is_official:
            return "VALID_UPSTREAM_PR", f"Valid PR #{pr_id} on {owner}/{repo}"
        else:
            return "PR_ON_UNOFFICIAL_REPO", f"PR #{pr_id} on unofficial repo {owner}/{repo}"

    # Check if repo: github.com/{owner}/{repo}
    repo_match = re.search(r"github\.com/([^/]+)/([^/]+)", clean, re.IGNORECASE)
    if repo_match:
        owner = repo_match.group(1).lower()
        repo = repo_match.group(2).lower()
        if owner in OFFICIAL_ORGS:
            return "BASE_REPO_NO_PR", f"Base official repo submitted without a PR: {owner}/{repo}"
        elif any(r in repo for r in OFFICIAL_REPOS):
            return "FORK_NO_PR", f"Personal fork of official repo without an upstream PR: {owner}/{repo}"
        else:
            return "UNOFFICIAL_REPO", f"Personal standalone repo: {owner}/{repo}"
            
    return "MALFORMED_URL", f"Malformed GitHub URL: {url}"

with get_db() as conn:
    print("=== EXECUTING SUBMISSION QUEUE TRIAGE ON PRODUCTION EC2 ===")
    
    # 1. APPROVED SUBMISSIONS
    approved_map = {
        73: ("Gurveer Singh", 82, "Milestone deliverable verified. PR #35 merged into Alkame core. Gate 4 cleared."),
        41: ("Kundan kumhar", 80, "Milestone deliverable verified. PR #16 merged into Internship Portal. Gate 4 cleared."),
        76: ("Ankur Sen", 84, "Milestone deliverable verified. Analytics upgrade layer PR #7 merged into Alkame core. Gate 4 cleared."),
        91: ("Shruthi Yuvnuv", 84, "Full-stack Aivara agentic workflow engine (+786 lines, clean test suite) verified and approved. Gate 4 cleared."),
        80: ("SHANU SRI GOWTHAM", 80, "Constraints engine and documentation additions (+913 lines) verified and approved. Gate 4 cleared.")
    }
    
    approved_count = 0
    for sub_id, (name, score, feedback) in approved_map.items():
        conn.execute("""
            UPDATE task_submissions
            SET status = 'approved',
                ai_evaluation_status = 'passed',
                ai_evaluation_score = ?,
                ai_evaluation_notes = ?
            WHERE id = ?;
        """, (score, feedback, sub_id))
        
        # Get intern_id for notification
        row = conn.execute("SELECT intern_id FROM task_submissions WHERE id = ?", (sub_id,)).fetchone()
        if row and row['intern_id']:
            conn.execute("""
                INSERT INTO notifications (intern_id, title, body, is_read, created_at)
                VALUES (?, 'Capstone Milestone Approved! (Gate 4 Cleared)', ?, 0, NOW());
            """, (row['intern_id'], feedback))
        
        approved_count += 1
        print(f"✅ Approved Sub #{sub_id} for {name} (Score: {score})")

    # 2. BHARGAVI C K (Merge Conflict in PR #36)
    bhargavi_feedback = (
        "Your PR contains 2,801 lines of valuable ML feature engineering, but currently has a git merge conflict "
        "with the main branch in feature_engineer.py. Please rebase against upstream main and resolve conflicts to proceed to approval."
    )
    conn.execute("""
        UPDATE task_submissions
        SET status = 'changes_requested',
            ai_evaluation_status = 'revision_needed',
            ai_evaluation_notes = ?
        WHERE id = 86;
    """, (bhargavi_feedback,))
    row = conn.execute("SELECT intern_id FROM task_submissions WHERE id = 86;").fetchone()
    if row and row['intern_id']:
        conn.execute("""
            INSERT INTO notifications (intern_id, title, body, is_read, created_at)
            VALUES (?, 'Action Required: Resolve Git Merge Conflict in PR #36', ?, 0, NOW());
        """, (row['intern_id'], bhargavi_feedback))
    print("⚠️ Set Sub #86 (Bhargavi C K) to changes_requested (Rebase needed)")

    # 3. BURRA THANVESH (Fork with valid commits)
    thanvesh_feedback = (
        "We verified your commits ('Fix authentication regression tests and CSV sanitization'). However, your work is on "
        "your personal fork. Please open an upstream Pull Request against DBERT-INDIA/Internshipportal to get approved immediately."
    )
    conn.execute("""
        UPDATE task_submissions
        SET status = 'changes_requested',
            ai_evaluation_status = 'revision_needed',
            ai_evaluation_notes = ?
        WHERE id = 85;
    """, (thanvesh_feedback,))
    row = conn.execute("SELECT intern_id FROM task_submissions WHERE id = 85;").fetchone()
    if row and row['intern_id']:
        conn.execute("""
            INSERT INTO notifications (intern_id, title, body, is_read, created_at)
            VALUES (?, 'Action Required: Open Upstream Pull Request to Clear Gate 4', ?, 0, NOW());
        """, (row['intern_id'], thanvesh_feedback))
    print("⚠️ Set Sub #85 (Burra Thanvesh) to changes_requested (Open upstream PR)")

    # 4. GURKA VINAY KUMAR REDDY (Fork with Dockerfile commits)
    vinay_feedback = (
        "Dockerfile and cloud port binding commits verified in your fork. Please open an upstream Pull Request against "
        "Gayatri-Education/Gayatri-AI to complete Gate 4 clearance."
    )
    conn.execute("""
        UPDATE task_submissions
        SET status = 'changes_requested',
            ai_evaluation_status = 'revision_needed',
            ai_evaluation_notes = ?
        WHERE intern_id = 4349 AND status != 'approved';
    """, (vinay_feedback,))
    conn.execute("""
        INSERT INTO notifications (intern_id, title, body, is_read, created_at)
        VALUES (4349, 'Action Required: Open Upstream Pull Request to Clear Gate 4', ?, 0, NOW());
    """, (vinay_feedback,))
    print("⚠️ Set Vinay Kumar Reddy's submission to changes_requested (Open upstream PR)")

    # 5. BATCH TRIAGE ALL REMAINING PENDING SUBMISSIONS
    # Fetch all other pending submissions
    pending_rows = conn.execute("""
        SELECT s.id, s.intern_id, s.github_repo_url, a.name, a.email
        FROM task_submissions s
        LEFT JOIN intern_accounts a ON a.id = s.intern_id
        WHERE s.status = 'pending' AND s.id NOT IN (73, 41, 76, 91, 80, 86, 85);
    """).fetchall()
    
    zero_commit_forks = [72, 90, 89, 81] # Aryan Bhakuni, Jay Kumar, Vansh Choudhary, Smit Shah
    
    triage_count = 0
    for r in pending_rows:
        s_id = r['id']
        i_id = r['intern_id']
        url = r['github_repo_url']
        classification, desc = classify_github(url)
        
        if s_id in zero_commit_forks or classification == 'FORK_NO_PR':
            fb = (
                "Your submitted GitHub repository link is a personal fork with zero new commits. To clear Gate 4, "
                "you must implement meaningful feature/bugfix code and open an upstream Pull Request against the official repository."
            )
            title = "Action Required: Code Contribution Required on Official Repository"
        elif classification == 'BASE_REPO_NO_PR':
            fb = (
                "You submitted the root link to our official repository without an individual branch or Pull Request. "
                "Please fork the repository, commit your project code on a feature branch, and submit your Pull Request link."
            )
            title = "Action Required: Individual Pull Request Required"
        elif classification == 'UNOFFICIAL_REPO':
            fb = (
                "Your submitted repository is a standalone personal project. Gate 4 requires a merged or approved Pull Request "
                "on one of our 4 official project repositories (Alkame, Gayatri, Aivara, Internship Portal). Please navigate to "
                "/stipend/tasks to select an official project task."
            )
            title = "Action Required: Submit Upstream PR on Official Project Repos"
        else: # MISSING or MALFORMED
            fb = (
                "No valid GitHub Pull Request link was provided with your submission. Please push your code to GitHub, "
                "open a Pull Request on the project repository, and submit the PR URL on /stipend/tasks."
            )
            title = "Action Required: GitHub Pull Request Link Missing"

        conn.execute("""
            UPDATE task_submissions
            SET status = 'changes_requested',
                ai_evaluation_status = 'revision_needed',
                ai_evaluation_notes = ?
            WHERE id = ?;
        """, (fb, s_id))
        
        if i_id:
            conn.execute("""
                INSERT INTO notifications (intern_id, title, body, is_read, created_at)
                VALUES (?, ?, ?, 0, NOW());
            """, (i_id, title, fb))
        
        triage_count += 1

    conn.commit()
    print(f"\n🎉 Successfully processed and triaged {triage_count} remaining pending submissions into changes_requested with tailored feedback.")

    # 6. VERIFICATION SUMMARY
    counts = conn.execute("""
        SELECT status, count(*) 
        FROM task_submissions 
        GROUP BY status;
    """).fetchall()
    print("\n=== UPDATED SUBMISSION COUNTS IN POSTGRESQL ===")
    for c in counts:
        print(f"  {c[0]}: {c[1]}")
