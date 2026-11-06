import csv
from collections import defaultdict

TSV_FILE = r"c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_m1_1\fast_matches.tsv"
OUT_FILE = r"c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_m1_1\all_grouped_matches.txt"

grouped = defaultdict(list)

with open(TSV_FILE, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        path = row["FilePath"]
        line_no = int(row["LineNumber"])
        snippet = row["Snippet"]
        grouped[path].append((line_no, snippet))

with open(OUT_FILE, "w", encoding="utf-8") as out:
    for path in sorted(grouped.keys()):
        items = grouped[path]
        out.write(f"FILE: {path} ({len(items)} occurrences)\n")
        for lno, snip in items:
            out.write(f"  Line {lno}: {snip}\n")
        out.write("\n")

print(f"Written grouped matches for {len(grouped)} files.")
