import csv, json, os, glob

def read_csv(path):
    rows = []
    with open(path, encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        for r in reader:
            if r:
                rows.append(r)
    return rows

print("--- TRAFFIC ACQUISITION ---")
ta_rows = read_csv("data/google/Traffic_acquisition_Session_primary_channel_group_(Default_channel_group).csv")
for r in ta_rows[:15]:
    print(r)

print("\n--- DEVICES ---")
dev_rows = read_csv("data/google/Devices.csv")
for r in dev_rows:
    print(r)

print("\n--- COUNTRIES TOP 10 ---")
c_rows = read_csv("data/google/Countries.csv")
for r in c_rows[:10]:
    print(r)

print("\n--- QUERIES TOP 15 ---")
q_rows = read_csv("data/google/Queries.csv")
for r in q_rows[:16]:
    print(r)

print("\n--- PAGES TOP 15 ---")
p_rows = read_csv("data/google/Pages.csv")
for r in p_rows[:16]:
    print(r)
