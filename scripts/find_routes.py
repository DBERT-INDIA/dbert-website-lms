with open("apps/portal/app.py", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if line.startswith("@app.route("):
            r = line.strip()
            if any(k in r for k in ["dashboard", "stipend", "wizard", "enroll", "index", "/portal"]):
                print(f"Line {i+1}: {r}")
