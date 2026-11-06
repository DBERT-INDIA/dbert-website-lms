import os
import re

valid_routes = set()
app_dir = os.path.join("apps", "website", "src", "app")
for root, dirs, files in os.walk(app_dir):
    for f in files:
        if f in ("page.tsx", "page.jsx", "route.ts", "route.js"):
            rel = os.path.relpath(root, app_dir).replace("\\", "/")
            if rel == ".":
                valid_routes.add("/")
            else:
                route = "/" + rel
                valid_routes.add(route)
                parts = route.split("/")
                clean_parts = [p for p in parts if not (p.startswith("[") and p.endswith("]"))]
                valid_routes.add("/".join(clean_parts))

print(f"Total valid Next.js app routes: {len(valid_routes)}")

# LMS portal routes or common external anchors
allowed_external = {
    "/courses", "/tasks", "/jobs", "/internships", "/portal", "/#signin",
    "/mentors/slots", "/cert/verify", "/mentors", "/admin", "/login"
}

links_found = set()
src_dir = os.path.join("apps", "website", "src")
for root, dirs, files in os.walk(src_dir):
    for f in files:
        if f.endswith((".tsx", ".ts", ".jsx", ".js", ".json")):
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                content = fp.read()
                matches = re.findall(r'href=[\'"](/[^#\'"?\s]*)', content)
                for m in matches:
                    links_found.add((m, os.path.relpath(path, src_dir)))

print(f"Total distinct internal links found in website src/: {len(links_found)}")
broken = []
for link, source_file in sorted(links_found):
    if link in ("/", ""):
        continue
    if link.startswith(("/_next", "/images", "/icons", "/logos", "/assets", "/favicon", "/fonts", "/docs", "/cv")):
        continue
    if any(link == x or link.startswith(x + "/") for x in allowed_external):
        continue

    # Check match
    match = False
    for vr in valid_routes:
        if link == vr:
            match = True
            break
        if "/[" in vr:
            prefix = vr.split("/[")[0]
            if link.startswith(prefix + "/"):
                match = True
                break

    if not match:
        broken.append((link, source_file))

print(f"Potentially dead / broken links: {len(broken)}")
for b, s in broken:
    print(f"  {b}  (found in: {s})")

print("\n--- Client fetch calls to /api/ ---")
api_calls = set()
for root, dirs, files in os.walk(src_dir):
    for f in files:
        if f.endswith((".tsx", ".ts")):
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                c = fp.read()
                matches = re.findall(r'fetch\([\'"](/api/[^\'"]*)[\'"]', c)
                for m in matches:
                    api_calls.add((m, f))

for call, f in sorted(api_calls):
    print(f"  {call}  (in {f})")
