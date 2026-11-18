import json

with open("data/ec2_existing_4courses_7day.json", "r", encoding="utf-8") as f:
    ec2_courses = json.load(f)

def format_course_code(c):
    var_name = c["domain"].upper().replace(" ", "_").replace("&", "AND") + "_COURSE"
    lines = [f"{var_name} = {{"]
    lines.append(f'    "domain": {json.dumps(c["domain"])},')
    lines.append(f'    "title": {json.dumps(c["title"])},')
    lines.append(f'    "slug": {json.dumps(c["slug"])},')
    lines.append(f'    "level": {json.dumps(c.get("level") or "Intermediate")},')
    lines.append(f'    "estimated_hours": {c.get("estimated_hours") or 14},')
    lines.append(f'    "banner_gradient": {json.dumps(c.get("banner_gradient") or "linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%)")},')
    lines.append('    "chapters": [')

    for ch in c["chapters"]:
        lines.append('        {')
        lines.append(f'            "day_number": {ch["day_number"]},')
        lines.append(f'            "title": {json.dumps(ch["title"])},')
        lines.append('            "subtopics": [')
        for s in ch["subtopics"]:
            takes = s["key_takeaways_json"]
            if isinstance(takes, str):
                try:
                    takes = json.loads(takes)
                except Exception:
                    takes = [takes]
            lines.append('                (')
            lines.append(f'                    {json.dumps(s["title"])},')
            lines.append(f'                    {json.dumps(s["brief"])},')
            lines.append(f'                    {json.dumps(takes)}')
            lines.append('                ),')
        lines.append('            ],')
        lines.append('            "quiz": [')
        for q in ch.get("quiz") or []:
            q_clean = {
                "id": q.get("id", 1),
                "question": q["question"],
                "options": q["options"],
                "correct_index": q.get("correct_index", 0)
            }
            lines.append('                ' + json.dumps(q_clean) + ',')
        lines.append('            ]')
        lines.append('        },')

    lines.append('    ]')
    lines.append('}')
    return "\n".join(lines)

# Read the current courses_7day_catalog.py
with open("apps/portal/config/courses_7day_catalog.py", "r", encoding="utf-8") as f:
    current_catalog = f.read()

# Build the 4 courses text
four_courses_code = "\n\n".join(format_course_code(c) for c in ec2_courses)

# Check if already has EXISTING_4_DOMAIN_COURSES
if "EXISTING_4_DOMAIN_COURSES" not in current_catalog:
    # Append the 4 courses before or after the 5 courses
    export_block = """

# ── Master Exports for All 9 Platform Domains (7-Day Production Curricula) ──
EXISTING_4_DOMAIN_COURSES = [
    DATA_ANALYST_COURSE,
    AI_AGENT_DEVELOPMENT_COURSE,
    FULL_STACK_DEVELOPMENT_COURSE,
    PYTHON_AUTOMATION_COURSE,
]

ALL_9_DOMAIN_COURSES = EXISTING_4_DOMAIN_COURSES + NEW_7DAY_DOMAIN_COURSES
"""
    new_content = current_catalog + "\n\n# ================================================================================\n# 4 Existing Platform Courses (Days 1–7 Synchronized from Production EC2)\n# ================================================================================\n\n" + four_courses_code + export_block
    with open("apps/portal/config/courses_7day_catalog.py", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully added 4 EC2 courses to courses_7day_catalog.py! Total courses defined: 9")
else:
    print("Catalog already contains EXISTING_4_DOMAIN_COURSES.")
