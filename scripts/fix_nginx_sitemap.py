import subprocess
import os

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
LOCAL_CONF = r"c:\Users\user\Desktop\dbert-website-lms\temp_dbert_nginx.conf"

def main():
    # 1. Download current file
    scp_down = [
        "scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes",
        f"{HOST}:/etc/nginx/sites-available/dbert-unified.conf", LOCAL_CONF
    ]
    res1 = subprocess.run(scp_down, capture_output=True, text=True)
    if res1.returncode != 0:
        print("SCP Down failed:", res1.stderr)
        return

    with open(LOCAL_CONF, "r", encoding="utf-8") as f:
        content = f.read()

    # Clean up any bad /sitemap-lms.xml block if present
    bad_pattern = """    # LMS Sitemap Proxy under main domain for Google Search Console URL-prefix property
    location = /sitemap-lms.xml {
        proxy_pass http://127.0.0.1:5001/sitemap.xml;
        proxy_set_header Host lms.dbert.in;
        proxy_set_header X-Real-IP ;
        proxy_set_header X-Forwarded-For ;
        proxy_set_header X-Forwarded-Proto ;
    }"""
    if bad_pattern in content:
        content = content.replace(bad_pattern, "")

    # Clean any other sitemap-lms block
    import re
    content = re.sub(r"\s*# LMS Sitemap Proxy[^\n]*\n\s*location = /sitemap-lms\.xml \{[^\}]*\}", "", content)

    # Insert correct block
    proper_block = """
    # LMS Sitemap Proxy under main domain for Google Search Console URL-prefix property
    location = /sitemap-lms.xml {
        proxy_pass http://127.0.0.1:5001/sitemap.xml;
        proxy_set_header Host lms.dbert.in;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
"""
    target = "    # Custom 404 Error Handling (Finding R3-01)"
    if target in content:
        content = content.replace(target, proper_block + "    # Custom 404 Error Handling (Finding R3-01)")
    else:
        print("Target not found")
        return

    with open(LOCAL_CONF, "w", encoding="utf-8") as f:
        f.write(content)

    # 2. Upload to remote /tmp
    scp_up = [
        "scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes",
        LOCAL_CONF, f"{HOST}:/tmp/dbert-unified.conf"
    ]
    res2 = subprocess.run(scp_up, capture_output=True, text=True)
    if res2.returncode != 0:
        print("SCP Up failed:", res2.stderr)
        return

    # 3. Move to /etc/nginx/sites-available, test and reload
    remote_cmd = (
        "sudo cp /tmp/dbert-unified.conf /etc/nginx/sites-available/dbert-unified.conf && "
        "sudo nginx -t && sudo systemctl reload nginx"
    )
    ssh_run = [
        "ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes",
        HOST, remote_cmd
    ]
    res3 = subprocess.run(ssh_run, capture_output=True, text=True)
    print("STDOUT:", res3.stdout)
    print("STDERR:", res3.stderr)
    print("Return code:", res3.returncode)

    if os.path.exists(LOCAL_CONF):
        os.remove(LOCAL_CONF)

if __name__ == "__main__":
    main()
