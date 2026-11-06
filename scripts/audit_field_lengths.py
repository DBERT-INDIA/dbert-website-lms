import csv

with open('sheet_data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Total candidates: {len(rows)}")

max_name = max(rows, key=lambda r: len(r.get('Name', '')))
max_college = max(rows, key=lambda r: len(r.get('College Name', '')))
max_domain = max(rows, key=lambda r: len(r.get('Select Internship', '')))
max_project = max(rows, key=lambda r: len(r.get('Project Contibuted On', '')))
max_batch = max(rows, key=lambda r: len(r.get('Choose Internship Batch', '')))

print(f"Max Name ({len(max_name.get('Name', ''))} chars): {max_name.get('Name', '')}")
print(f"Max College ({len(max_college.get('College Name', ''))} chars): {max_college.get('College Name', '')}")
print(f"Max Domain ({len(max_domain.get('Select Internship', ''))} chars): {max_domain.get('Select Internship', '')}")
print(f"Max Project ({len(max_project.get('Project Contibuted On', ''))} chars): {max_project.get('Project Contibuted On', '')}")
print(f"Max Batch ({len(max_batch.get('Choose Internship Batch', ''))} chars): {max_batch.get('Choose Internship Batch', '')}")

print("\n--- Distribution of Domains ---")
domains = {}
for r in rows:
    d = r.get('Select Internship', '').strip()
    domains[d] = domains.get(d, 0) + 1
for k, v in domains.items():
    print(f"  {k}: {v}")

print("\n--- Longest 5 College Names ---")
sorted_colleges = sorted(rows, key=lambda r: len(r.get('College Name', '')), reverse=True)[:5]
for r in sorted_colleges:
    print(f"  [{len(r.get('College Name', ''))} chars] {r.get('Name')}: {r.get('College Name')}")

print("\n--- Longest 5 Project Descriptions ---")
sorted_projects = sorted(rows, key=lambda r: len(r.get('Project Contibuted On', '')), reverse=True)[:5]
for r in sorted_projects:
    print(f"  [{len(r.get('Project Contibuted On', ''))} chars] {r.get('Name')}: {r.get('Project Contibuted On')}")
