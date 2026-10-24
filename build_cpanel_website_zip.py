import os
import zipfile

source_dir = os.path.abspath('apps/website/out')
output_zip = os.path.abspath('dbert_website_static.zip')

print(f"Packaging {source_dir} -> {output_zip} with Unix permissions (755 dirs / 644 files)...")

count_files = 0
count_dirs = 0

with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(source_dir):
        for d in dirs:
            full_dir = os.path.join(root, d)
            rel_dir = os.path.relpath(full_dir, source_dir).replace('\\', '/') + '/'
            zinfo = zipfile.ZipInfo(rel_dir)
            zinfo.create_system = 3  # Unix
            zinfo.external_attr = ((0o040000 | 0o755) << 16) | 0x10  # Directory with 0755
            zipf.writestr(zinfo, '')
            count_dirs += 1
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, source_dir).replace('\\', '/')
            with open(full_path, 'rb') as fp:
                data = fp.read()
            zinfo = zipfile.ZipInfo(rel_path)
            zinfo.create_system = 3  # Unix
            zinfo.external_attr = (0o100000 | 0o644) << 16  # Regular file with 0644
            zipf.writestr(zinfo, data)
            count_files += 1

size_mb = os.path.getsize(output_zip) / (1024 * 1024)
print(f"Successfully packaged {count_files} files and {count_dirs} directories ({size_mb:.2f} MB).")
