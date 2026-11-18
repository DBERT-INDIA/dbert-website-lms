import json

fn = "C:/Users/user/.gemini/antigravity/brain/db340522-3de4-46ab-8736-005fb1623326/.system_generated/logs/transcript_full.jsonl"
with open(fn, "r", encoding="utf-8") as f:
    for line in f:
        if '"step_index": 197' in line or '"step_index":197' in line:
            obj = json.loads(line)
            tool_calls = obj.get("tool_calls", [])
            for tc in tool_calls:
                args = tc.get("args", {})
                replacement = args.get("Replacement", "")
                if "get_or_create_offer_letter" in replacement:
                    print("Found replacement! Length:", len(replacement))
                    with open("recovered_offer_block.py", "w", encoding="utf-8") as out:
                        out.write(replacement)
            break
print("Done extracting.")
