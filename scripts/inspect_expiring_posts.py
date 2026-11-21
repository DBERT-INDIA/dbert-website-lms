import json

with open("data/expiring_43_posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

print(f"Total posts: {len(posts)}")
for p in posts:
    print(f"ID {p['id']:3d} | {p['post_type']:10s} | {p['domain']:22s} | {p['title']}")
