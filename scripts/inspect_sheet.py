import csv

with open('sheet_data.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    headers = [h.strip() for h in next(reader)]
    rows = []
    for r in reader:
        if r and any(cell.strip() for cell in r):
            rows.append(r)

print(f"Total non-empty data rows: {len(rows)}")
print("Headers:", headers)
print("-" * 80)
for i, r in enumerate(rows):
    row_dict = {h: val.strip() for h, val in zip(headers, r)}
    name = row_dict.get("Name", "")
    email = row_dict.get("Email Address", "")
    domain = row_dict.get("Select Internship", "")
    batch = row_dict.get("Choose Internship Batch", "")
    college = row_dict.get("College Name", "")
    project = row_dict.get("Project Contibuted On", "")
    print(f"[{i+1:02d}] {name} | {email} | {domain} | {batch} | {college} | {project}")
