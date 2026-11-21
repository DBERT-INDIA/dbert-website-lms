import os
import sys
import json
import shutil
import subprocess
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.abspath("scripts"))

from generate_sample_packet import (
    draw_cert_completion,
    draw_cert_evaluation,
    draw_cert_lor,
    safe_save_canvas,
    BASE_DIR
)

OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs", "cohort_2026")
WEBSITE_PREVIEWS_DIR = os.path.join(BASE_DIR, "apps", "website", "public", "certificates", "previews")
REGISTRY_FILE = os.path.join(BASE_DIR, "apps", "website", "src", "data", "certificates_registry.json")
DIRECTORY_FILE = os.path.join(BASE_DIR, "apps", "website", "src", "data", "directory_candidates.json")
VERIFICATION_SUBMISSIONS_FILE = os.path.join(BASE_DIR, "data", "verification_submissions_299.json")

os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(WEBSITE_PREVIEWS_DIR, exist_ok=True)

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

# 1. Fetch latest verification_submissions_299.json from EC2
print("Fetching latest verification_submissions_299.json from EC2...")
res = subprocess.run(
    ["ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", REMOTE_HOST, "cat /var/www/dbert-website-lms/data/verification_submissions_299.json"],
    capture_output=True,
    text=True
)
if res.returncode != 0:
    print("Failed to fetch from EC2:", res.stderr)
    sys.exit(1)

subs = json.loads(res.stdout)
print(f"Total submissions fetched: {len(subs)}")

# Load Registry and Directory
with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
    registry = json.load(f)

with open(DIRECTORY_FILE, "r", encoding="utf-8") as f:
    directory = json.load(f)

dir_map = {item.get("certId"): item for item in directory if item.get("certId")}

# 2. Generate 3-doc packet for Devanshi Yadav (CERT-DBERT-2026-UIUX-036)
DEVANSHI_DATA = {
    "index": 76,
    "name": "Devanshi Yadav",
    "email": "devanshiyadav9131@gmail.com",
    "phone": "9131976077",
    "college": "South Asian University",
    "domain": "UI/UX Design",
    "batch": "July to Sep 2026",
    "project": "Gayatri AI — Enterprise Educational Intelligence Platform",
    "topics": "Figma, User Research, Wireframing, High-Fidelity Prototyping, Usability Testing, Visual Design Systems",
    "duration": "15 July 2026 – 15 September 2026 (2 Months)",
    "start_date": "July 2026",
    "end_date": "September 2026",
    "eval_date": "15 September 2026",
    "issue_date": "2026-11-04",
    "cert_id": "CERT-DBERT-2026-UIUX-036",
    "intern_id": "DBERT-2026-INT-1161",
    "score": 83,
    "grade": "Grade: A (Very Good Performance)",
    "rubric_marks": [17, 8, 8, 8, 9, 8, 9, 8, 8],
    "source": "Website 299 Payment (UTR 478130342751)"
}

cand_dir = os.path.join(OUTPUTS_DIR, "76_devanshi_yadav")
os.makedirs(cand_dir, exist_ok=True)
doc1_pdf = os.path.join(cand_dir, "1_Certificate_of_Completion_CERT-DBERT-2026-UIUX-036.pdf")
doc2_pdf = os.path.join(cand_dir, "2_Academic_Project_Evaluation_CERT-DBERT-2026-UIUX-036.pdf")
doc3_pdf = os.path.join(cand_dir, "3_Letter_of_Recommendation_CERT-DBERT-2026-UIUX-036.pdf")

print("\nGenerating 3-Document Dossier for Devanshi Yadav...")
safe_save_canvas(None, doc1_pdf, draw_cert_completion, DEVANSHI_DATA)
safe_save_canvas(None, doc2_pdf, draw_cert_evaluation, DEVANSHI_DATA)
safe_save_canvas(None, doc3_pdf, draw_cert_lor, DEVANSHI_DATA)

# Copy preview PNG
doc1_png = doc1_pdf.replace(".pdf", ".png")
pub_png = os.path.join(WEBSITE_PREVIEWS_DIR, "CERT-DBERT-2026-UIUX-036.png")
if os.path.exists(doc1_png):
    shutil.copy2(doc1_png, pub_png)
    print(f"  Preview PNG copied to: {pub_png}")
else:
    print(f"  Warning: {doc1_png} not found to copy to {pub_png}")

# 3. Process Target Submissions: #22, #23, #24, #25 (0-indexed 21, 22, 23, 24)
target_cids = [
    "CERT-DBERT-2026-FSD-042",   # Suraj Shivsunder Jha
    "CERT-DBERT-2026-UIUX-036",  # Devanshi Yadav
    "CERT-DBERT-2026-AIML-169",  # G.Vinay Kumar Reddy
    "CERT-DBERT-2026-DA-112"     # Bharathan K
]

# Update submissions status to APPROVED
for s in subs:
    cid = s.get("certId")
    if cid in target_cids:
        s["status"] = "APPROVED"
        print(f"Marked submission {cid} ({s.get('fullName')}) as APPROVED.")

# Update certificates_registry.json
for cid in target_cids:
    if cid in registry:
        c_rec = registry[cid]
        c_rec["verified"] = True
        c_rec["isProvisional"] = False
        c_rec["status"] = "VERIFIED"
        c_rec["verificationDate"] = "2026-11-20"
        c_rec["previewUrl"] = f"/certificates/previews/{cid}.png"
        if cid == "CERT-DBERT-2026-UIUX-036":
            c_rec["doc1Pdf"] = doc1_pdf
            c_rec["doc2Pdf"] = doc2_pdf
            c_rec["doc3Pdf"] = doc3_pdf
            c_rec["topics"] = DEVANSHI_DATA["topics"]
            c_rec["score"] = DEVANSHI_DATA["score"]
            c_rec["grade"] = DEVANSHI_DATA["grade"]
        print(f"Updated Registry for {cid}: status=VERIFIED, isProvisional=False")

# Update directory_candidates.json
for cid in target_cids:
    reg_entry = registry.get(cid, {})
    if cid in dir_map:
        d_rec = dir_map[cid]
        d_rec["status"] = "VERIFIED"
        d_rec["verified"] = True
        d_rec["isProvisional"] = False
        d_rec["previewUrl"] = f"/certificates/previews/{cid}.png"
        print(f"Updated Directory for {cid}: Tab 1 Pre-Vetted (status=VERIFIED)")
    else:
        # Create new directory entry
        new_dir_entry = {
            "certId": cid,
            "holderName": reg_entry.get("holderName"),
            "email": reg_entry.get("email"),
            "college": reg_entry.get("college"),
            "domain": reg_entry.get("domain"),
            "score": reg_entry.get("score"),
            "status": "VERIFIED",
            "verified": True,
            "isProvisional": False,
            "previewUrl": f"/certificates/previews/{cid}.png"
        }
        directory.append(new_dir_entry)
        dir_map[cid] = new_dir_entry
        print(f"Added to Directory for {cid}: Tab 1 Pre-Vetted (status=VERIFIED)")

# Save updated files
with open(VERIFICATION_SUBMISSIONS_FILE, "w", encoding="utf-8") as f:
    json.dump(subs, f, indent=2, ensure_ascii=False)
print(f"Saved {VERIFICATION_SUBMISSIONS_FILE} ({len(subs)} submissions).")

with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
    json.dump(registry, f, indent=2, ensure_ascii=False)
print(f"Saved {REGISTRY_FILE} ({len(registry)} certificates).")

with open(DIRECTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(directory, f, indent=2, ensure_ascii=False)
print(f"Saved {DIRECTORY_FILE} ({len(directory)} candidates).")
