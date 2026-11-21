import json

with open("data/top_targets_299.json", "r", encoding="utf-8") as f:
    t299 = json.load(f)

with open("data/top_targets_499.json", "r", encoding="utf-8") as f:
    t499 = json.load(f)

# Clean fields
clean_299 = []
for x in t299[:25]:
    cert_id = x.get("cert_info", {}).get("certId", "") if x.get("cert_info") else ""
    clean_299.append({
        "id": x["id"],
        "name": x["name"],
        "email": x["email"],
        "phone": x.get("phone") or "",
        "domain": x.get("domain") or "Engineering",
        "certId": cert_id,
        "isProvisional": x.get("is_cert_provisional", False),
        "hasUpi": x.get("has_upi", False),
        "logins": x.get("login_count", 0),
        "tasks": x.get("tasks_count", 0),
        "apps": x.get("apps_count", 0),
        "score": x.get("intent_score", 50),
        "reasons": x.get("intent_reasons", []),
        "unlockUrl": f"https://dbert.in/verify/unlock?email={x['email']}" + (f"&certid={cert_id}" if cert_id else "")
    })

clean_499 = []
for x in t499[:30]:
    clean_499.append({
        "id": x["id"],
        "name": x["name"],
        "email": x["email"],
        "phone": x.get("phone") or "",
        "domain": x.get("domain") or "Engineering",
        "stage": x.get("signup_stage", "3"),
        "status": x.get("account_status", "Selected"),
        "logins": x.get("login_count", 0),
        "apps": x.get("apps_count", 0),
        "score": x.get("caution_score", 60),
        "reasons": x.get("caution_reasons", []),
        "offerUrl": f"https://lms.dbert.in/portal/offer?email={x['email']}"
    })

print("Formatted JSON ready:")
print(f"299 list: {len(clean_299)}")
print(f"499 list: {len(clean_499)}")

with open("data/clean_299_embed.json", "w", encoding="utf-8") as f:
    json.dump(clean_299, f)

with open("data/clean_499_embed.json", "w", encoding="utf-8") as f:
    json.dump(clean_499, f)
