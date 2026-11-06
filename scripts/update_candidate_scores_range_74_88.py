import json
import hashlib
import csv
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent

def get_score_and_grade(cert_id: str):
    h = int(hashlib.sha256(cert_id.encode('utf-8')).hexdigest()[:8], 16) % 10000
    score = (h % 15) + 74  # range 74 to 88 inclusive
    if score >= 85:
        grade = "Grade A+ (Outstanding)"
    elif score >= 80:
        grade = "Grade A (Very Good)"
    elif score >= 76:
        grade = "Grade B+ (Good)"
    else:
        grade = "Grade B (Above Average)"
    return score, grade

def main():
    print("=" * 76)
    print("UPDATING PROVISIONAL CANDIDATE SCORES TO RANDOMIZED RANGE 74–88")
    print("=" * 76)

    # 1. Update data/all_409_provisional_registry.json
    path_409_root = BASE_DIR / "data" / "all_409_provisional_registry.json"
    if path_409_root.exists():
        with open(path_409_root, "r", encoding="utf-8") as f:
            registry_409 = json.load(f)
        for cand in registry_409:
            score, grade = get_score_and_grade(cand["certId"])
            cand["score"] = score
            cand["grade"] = grade
        with open(path_409_root, "w", encoding="utf-8") as f:
            json.dump(registry_409, f, indent=2, ensure_ascii=False)
        print(f"✓ Updated {len(registry_409)} records in data/all_409_provisional_registry.json")

    # 2. Update apps/website/src/data/all_409_provisional_registry.json
    path_409_web = BASE_DIR / "apps" / "website" / "src" / "data" / "all_409_provisional_registry.json"
    if path_409_web.exists():
        with open(path_409_web, "w", encoding="utf-8") as f:
            json.dump(registry_409, f, indent=2, ensure_ascii=False)
        print(f"✓ Synchronized apps/website/src/data/all_409_provisional_registry.json")

    # 3. Update apps/website/src/data/directory_candidates.json
    path_dir = BASE_DIR / "apps" / "website" / "src" / "data" / "directory_candidates.json"
    if path_dir.exists():
        with open(path_dir, "r", encoding="utf-8") as f:
            dir_cands = json.load(f)
        updated_prov = 0
        for cand in dir_cands:
            if cand.get("isProvisional"):
                score, grade = get_score_and_grade(cand["certId"])
                cand["score"] = score
                cand["grade"] = grade
                updated_prov += 1
        with open(path_dir, "w", encoding="utf-8") as f:
            json.dump(dir_cands, f, indent=2, ensure_ascii=False)
        print(f"✓ Updated {updated_prov} provisional records in apps/website/src/data/directory_candidates.json")

    # 4. Update apps/website/src/data/certificates_registry.json
    path_certs = BASE_DIR / "apps" / "website" / "src" / "data" / "certificates_registry.json"
    if path_certs.exists():
        with open(path_certs, "r", encoding="utf-8") as f:
            certs_dict = json.load(f)
        updated_certs = 0
        for cert_id, cand in certs_dict.items():
            if cand.get("isProvisional") or cand.get("verified") is False or "provisional" in str(cand.get("status", "")).lower():
                score, grade = get_score_and_grade(cert_id)
                cand["score"] = score
                cand["grade"] = grade
                updated_certs += 1
        with open(path_certs, "w", encoding="utf-8") as f:
            json.dump(certs_dict, f, indent=2, ensure_ascii=False)
        print(f"✓ Updated {updated_certs} provisional records in certificates_registry.json")

    # 5. Update data/dispatch_tracking_409.json and reset the 5 rate-limited items
    path_tracking = BASE_DIR / "data" / "dispatch_tracking_409.json"
    if path_tracking.exists():
        with open(path_tracking, "r", encoding="utf-8") as f:
            tracking = json.load(f)
        reset_count = 0
        for item in tracking:
            score, grade = get_score_and_grade(item["certId"])
            item["score"] = score
            item["grade"] = grade
            # Reset rate-limited records back to PENDING
            if item.get("status") == "FAILED" and "Daily user sending limit exceeded" in str(item.get("error", "")):
                item["status"] = "PENDING"
                item["error"] = None
                reset_count += 1
        with open(path_tracking, "w", encoding="utf-8") as f:
            json.dump(tracking, f, indent=2, ensure_ascii=False)
        print(f"✓ Updated scores in dispatch_tracking_409.json (reset {reset_count} rate-limited items to PENDING)")

        # 6. Synchronize CSV
        path_csv = BASE_DIR / "data" / "dispatch_tracking_409.csv"
        fieldnames = [
            "index", "certId", "internId", "holderName", "email",
            "domain", "project", "duration", "score", "grade",
            "verifyUrl", "status", "sent_at", "message_id", "provider", "error"
        ]
        with open(path_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in tracking:
                writer.writerow(r)
        print("✓ Synchronized data/dispatch_tracking_409.csv")

    # Preview sample under letter 'A'
    with open(path_dir, "r", encoding="utf-8") as f:
        dir_cands = json.load(f)
    a_sample = [c for c in dir_cands if c.get("firstLetter") == "A"][:8]
    print("\nSample Preview under letter 'A':")
    for c in a_sample:
        print(f"  • {c['holderName']} ({c['certId']}): {c['score']}/100 ({c['grade']})")

if __name__ == "__main__":
    main()
