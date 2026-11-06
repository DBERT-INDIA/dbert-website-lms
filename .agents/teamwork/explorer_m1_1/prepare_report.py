import json
from collections import defaultdict

with open(".agents/teamwork/explorer_m1_1/audit_data.json", "r", encoding="utf-8") as f:
    findings = json.load(f)

# Group by category
blockers = [f for f in findings if f["classification"] == "Blocker"]
intentional = [f for f in findings if f["classification"] == "Intentional redirect rule"]
warnings = [f for f in findings if f["classification"] == "Warning"]

print(f"Blockers: {len(blockers)}, Intentional: {len(intentional)}, Warnings: {len(warnings)}")

# Check distinct files for blockers
blocker_files = defaultdict(list)
for b in blockers:
    blocker_files[b["file"]].append(b)

print(f"Blocker distinct files: {len(blocker_files)}")
