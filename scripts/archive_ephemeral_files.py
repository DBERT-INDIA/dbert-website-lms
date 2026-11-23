"""
scripts/archive_ephemeral_files.py
==================================
Safely moves completed batch queues, obsolete logs, and screenshots into data/archive/
while strictly safeguarding all 8 permanent master registries and active databases.
"""
import os
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
SCRIPTS_DIR = ROOT_DIR / "scripts"

ARCHIVE_QUEUES = DATA_DIR / "archive" / "queues"
ARCHIVE_LOGS = DATA_DIR / "archive" / "logs"
ARCHIVE_SHOTS = DATA_DIR / "archive" / "screenshots"
ARCHIVE_DIAGNOSTICS = SCRIPTS_DIR / "archive" / "diagnostics"

for d in [ARCHIVE_QUEUES, ARCHIVE_LOGS, ARCHIVE_SHOTS, ARCHIVE_DIAGNOSTICS]:
    d.mkdir(parents=True, exist_ok=True)

# 8 Permanent Master Registries + Active Databases (NEVER MOVE)
PRESERVED_FILES = {
    "all_409_provisional_registry.json",
    "balance_enrollments_1500.json",
    "verification_submissions_299.json",
    "dbert_whatsapp.db",
    "quota_watchdog_state.json",
    "sheet_1593_provisional_registry.json",
    "sheet_859_registry.json",
    "expiring_43_posts.json",
    # Active Databases & Omnichannel Tracking
    "dbert_revenue_whatsapp.db",
    "dbert_whatsapp_selected_16nov.db",
    "dispatch_tracking_409.json",
    "dispatch_tracking_409.csv",
    "dbert_unified_omnichannel_tracking.csv",
    "dbert_sheet_1593_omnichannel_tracking.csv",
    "sheet_1593_dispatch_tracking.json",
    "dispatch_tracking_sheet_859.json",
    "dbert_whatsapp_master.csv",
    "dbert_whatsapp_acc1.csv",
    "dbert_whatsapp_acc2.csv",
    "dispatch_tracking_batch35_acc2.csv",
    "dispatch_tracking_stipend_299.csv",
    "dispatch_tracking_selected_multi_login.csv",
    "dbert_whatsapp_sent_today.json"
}

# 1. Ephemeral queues to move
QUEUE_FILES = [
    "whatsapp_299_queue_acc1.json",
    "whatsapp_299_queue_acc2.json",
    "whatsapp_299_queue_batch35_acc2.json",
    "whatsapp_299_queue_batch35_live.json",
    "whatsapp_299_queue_batch35_next.json",
    "whatsapp_299_queue_master.json",
    "whatsapp_selected_multi_login_queue.json",
    "whatsapp_tier_b_and_guidance_queue.json",
    "whatsapp_unlocked_queue_acc1.json",
    "whatsapp_unlocked_queue_acc2.json",
    "whatsapp_unlocked_queue_retry.json",
    "whatsapp_unlocked_sent.json",
    "cohort_a_final.json",
    "cohort_b_final.json",
    "cohort_c_final.json",
    "cohort_d_final.json",
    "cohort_a_selected_unpaid.json",
    "cohort_b_rejected_payments.json",
    "cohort_c_pending_gates.json",
    "cohort_d_all_gates_verified.json",
    "cohort_299_multilogin_26.json",
    "cohort_499_multilogin_136.json",
    "cohort_discrepancy_10.json",
    "selected_multi_login_cohort.json"
]

# 2. Ephemeral logs to move
LOG_FILES = [
    "dispatch_11_stipend.log",
    "dispatch_13_sheet.log",
    "dispatch_149_selected.log",
    "dispatch_16nov_cohort.log",
    "dispatch_7_verified.log",
    "dispatch_9_verified.log",
    "dispatch_ambassador_outreach.log",
    "dispatch_incomplete_146.log",
    "dispatch_never_logged_2585.log",
    "dispatch_rejected_payments.log",
    "dispatch_selected_56.log",
    "whatsapp_dispatch_299.log",
    "whatsapp_dispatch_selected_multi_login.log",
    "whatsapp_dispatch_today.log",
    "whatsapp_stipend_10.log",
    "whatsapp_tier_b_guidance.log",
    "whatsapp_unlocked_dispatch.log",
    "cohort_dispatch.log",
    "dashboard_emails.log",
    "discrepancy_roadmap_dispatch.log",
    "dispatch_active_54h.log",
    "dispatch_revenue_100.log",
    "dispatch_revenue_whatsapp.log"
]

def run_archive():
    print("Beginning selective archiving...")
    moved_count = 0

    # Move queues
    for fname in QUEUE_FILES:
        fpath = DATA_DIR / fname
        if fpath.exists() and fname not in PRESERVED_FILES:
            shutil.move(str(fpath), str(ARCHIVE_QUEUES / fname))
            moved_count += 1
            print(f"Archived queue: {fname}")

    # Move logs
    for fname in LOG_FILES:
        fpath = DATA_DIR / fname
        if fpath.exists() and fname not in PRESERVED_FILES:
            shutil.move(str(fpath), str(ARCHIVE_LOGS / fname))
            moved_count += 1
            print(f"Archived log: {fname}")

    # Move debug screenshots
    for fpath in DATA_DIR.glob("*.png"):
        fname = fpath.name
        if fname not in PRESERVED_FILES:
            shutil.move(str(fpath), str(ARCHIVE_SHOTS / fname))
            moved_count += 1
            print(f"Archived screenshot: {fname}")

    print(f"\nArchiving complete! Safely moved {moved_count} ephemeral files.")
    print("Master registries verified untouched:")
    for reg in sorted(PRESERVED_FILES):
        p = DATA_DIR / reg
        print(f"  - {reg}: {'EXISTS (' + str(p.stat().st_size) + ' bytes)' if p.exists() else 'NOT FOUND'}")

if __name__ == "__main__":
    run_archive()
