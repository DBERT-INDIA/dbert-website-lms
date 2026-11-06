import os

root = r'c:\Users\user\Desktop\dbert-website-lms'
agent_dir = os.path.join(root, '.agents', 'teamwork', 'explorer_r1')
scan_path = os.path.join(agent_dir, 'clean_scan.txt')

cpanel_matches = []
with open(scan_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip('\r\n')
        if line.startswith('cpanel_public_html'):
            cpanel_matches.append(line)

print(f"Total cpanel_public_html matches: {len(cpanel_matches)}")
with open(os.path.join(agent_dir, 'cpanel_matches.txt'), 'w', encoding='utf-8') as out:
    for m in cpanel_matches:
        out.write(m + '\n')
