import os

root = r'c:\Users\user\Desktop\dbert-website-lms'
agent_dir = os.path.join(root, '.agents', 'teamwork', 'explorer_r1')

for base in ['cpanel_public_html', 'apps/website']:
    dir_path = os.path.join(root, base)
    total_files = 0
    files_with_online = 0
    files_with_schema_online = 0
    for dirpath, dirnames, filenames in os.walk(dir_path):
        if 'node_modules' in dirnames:
            dirnames.remove('node_modules')
        if '.next' in dirnames:
            dirnames.remove('.next')
        for fname in filenames:
            total_files += 1
            fpath = os.path.join(dirpath, fname)
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if 'dbert.online' in content:
                        files_with_online += 1
                        if '"url": "https://dbert.online"' in content or '"url":"https://dbert.online"' in content:
                            files_with_schema_online += 1
            except:
                pass
    print(f"Base {base}: total {total_files} files, {files_with_online} with 'dbert.online', {files_with_schema_online} with schema 'dbert.online'")
