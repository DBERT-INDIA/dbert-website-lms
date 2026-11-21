import json

with open("data/expiring_43_posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

for i, p in enumerate(posts, 1):
    print(f"{i:2d}. ID {p['id']:3d} | [{p['domain']:22s}] | Title: {p['title']}")
