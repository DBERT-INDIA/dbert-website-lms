import json
import os

with open("data/top_targets_299.json", "r", encoding="utf-8") as f:
    t299 = json.load(f)

with open("data/top_targets_499.json", "r", encoding="utf-8") as f:
    t499 = json.load(f)

print(f"Loaded {len(t299)} targets for 299 and {len(t499)} targets for 499.")
