import subprocess, os, sys

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"

def run_ssh(cmd):
    full_cmd = [
        "ssh", "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        HOST, cmd
    ]
    res = subprocess.run(full_cmd, capture_output=True, text=True)
    return res.stdout, res.stderr

cmds = [
    ("Uptime & Load", "uptime"),
    ("Nginx Access Log Total Lines", "sudo wc -l /var/log/nginx/access.log"),
    ("Top 10 Client IPs", "sudo awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -nr | head -n 10"),
    ("Top 20 Requested URIs", "sudo awk '{print $7}' /var/log/nginx/access.log | cut -d'?' -f1 | sort | uniq -c | sort -nr | head -n 20"),
    ("HTTP Status Codes Distribution", "sudo awk '{print $9}' /var/log/nginx/access.log | sort | uniq -c | sort -nr"),
    ("AI Crawler Requests", "grep -Eic 'gptbot|claudebot|perplexity|chatgpt|google-extended|bytespider|anthropic' /var/log/nginx/access.log || true"),
    ("Googlebot & Bingbot Requests", "grep -Eic 'googlebot|bingbot' /var/log/nginx/access.log || true"),
    ("Active Next.js Inbound Leads Count", "cat /var/www/dbert-website-lms/data/leads_inbound.json 2>/dev/null | wc -l || echo '0'"),
    ("Active Balance Submissions Count", "cat /var/www/dbert-website-lms/data/balance_enrollments_1500.json 2>/dev/null | grep -c 'submissionId' || echo '0'")
]

for title, cmd in cmds:
    out, err = run_ssh(cmd)
    print(f"=== {title} ===")
    print(out.strip())
    if err and not out:
        print("ERR:", err.strip())
