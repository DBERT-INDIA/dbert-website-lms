import os, time

files = [
    "apps/portal/services/delivery_service.py",
    "apps/portal/app.py",
    "scripts/verify_delivery_post_cooldown.py",
    ".agents/teamwork/challenger_delivery_1/adversarial_delivery_stress.py",
    ".agents/teamwork/challenger_delivery_2/test_stress_harness.py",
    "apps/portal/tests/test_delivery_service.py",
    "apps/portal/internship.db"
]

for f in files:
    if os.path.exists(f):
        mtime = os.path.getmtime(f)
        print(f"{f}: modified at {time.ctime(mtime)} ({time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(mtime))})")
    else:
        print(f"{f}: NOT FOUND")
