import os
import shutil
import sys

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
source_dir = os.path.join(root_dir, "apps", "website", "out")
dest_dir = os.path.join(root_dir, "cpanel_public_html")

print("=" * 70)
print("DBERT cPanel Static Frontend Staging Engine")
print(f"Source: {source_dir}")
print(f"Target: {dest_dir}")
print("=" * 70)

if not os.path.exists(source_dir):
    print(f"ERROR: Build directory not found: {source_dir}")
    print("Please run 'npm run build' inside apps/website first.")
    sys.exit(1)

# Clean and recreate target staging folder
if os.path.exists(dest_dir):
    print(f"Cleaning existing staging directory: {dest_dir}...")
    shutil.rmtree(dest_dir)

os.makedirs(dest_dir, exist_ok=True)

# Copy files
count_files = 0
count_dirs = 0
total_bytes = 0

for root, dirs, files in os.walk(source_dir):
    rel_root = os.path.relpath(root, source_dir)
    target_root = os.path.join(dest_dir, rel_root) if rel_root != "." else dest_dir

    for d in dirs:
        os.makedirs(os.path.join(target_root, d), exist_ok=True)
        count_dirs += 1

    for f in files:
        src_path = os.path.join(root, f)
        dst_path = os.path.join(target_root, f)
        shutil.copy2(src_path, dst_path)
        count_files += 1
        total_bytes += os.path.getsize(src_path)

# Authoritative .htaccess copy from apps/website/public/.htaccess
authoritative_htaccess = os.path.join(root_dir, "apps", "website", "public", ".htaccess")
htaccess_dst = os.path.join(dest_dir, ".htaccess")
if os.path.exists(authoritative_htaccess):
    shutil.copy2(authoritative_htaccess, htaccess_dst)
    # Also update apps/website/out/.htaccess for consistency
    out_htaccess = os.path.join(source_dir, ".htaccess")
    shutil.copy2(authoritative_htaccess, out_htaccess)

size_mb = total_bytes / (1024 * 1024)
print(f"\nSuccessfully staged {count_files} files and {count_dirs} directories ({size_mb:.2f} MB).")
print(f"Authoritative .htaccess present: {os.path.exists(htaccess_dst)}")
print(f"Robots.txt present: {os.path.exists(os.path.join(dest_dir, 'robots.txt'))}")
print(f"Sitemap.xml present: {os.path.exists(os.path.join(dest_dir, 'sitemap.xml'))}")
print(f"Index.html present: {os.path.exists(os.path.join(dest_dir, 'index.html'))}")
print(f"404.html present: {os.path.exists(os.path.join(dest_dir, '404.html'))}")
print("\n[READY] Upload the entire contents of this folder directly to your cPanel public_html/ via FileZilla:")
print(f"  --> {dest_dir}\n")
