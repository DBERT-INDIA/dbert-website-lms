import re

with open("ARCHITECTURE_ROADMAP.md", "r", encoding="utf-8") as f:
    text = f.read()

mermaid_blocks = re.findall(r"```mermaid\n(.*?)\n```", text, re.DOTALL)
print(f"Total diagrams: {len(mermaid_blocks)}")

issues = 0
for idx, b in enumerate(mermaid_blocks):
    lines = b.splitlines()
    for l_no, l in enumerate(lines):
        if "[" in l and "]" in l:
            label_match = re.findall(r"\[(.*?)\]", l)
            for lbl in label_match:
                if "(" in lbl or ")" in lbl:
                    if not (lbl.startswith('"') and lbl.endswith('"')):
                        print(f"Diagram {idx+1}, Line {l_no+1}: Unquoted parenthesis in [{lbl}]")
                        issues += 1

if issues == 0:
    print("PASS: All node labels with parenthesis are properly quoted!")
else:
    print(f"FAIL: Found {issues} unquoted labels.")
