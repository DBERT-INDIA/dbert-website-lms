# DBERT Ecosystem — FileZilla SFTP Deployment & EC2 Setup Guide
> Production Architecture: **`https://dbert.in`** (Next.js Node Service :3001) & **`https://lms.dbert.in`** (Flask / Gunicorn LMS :5001)

This guide walks you through deploying the complete DBERT web ecosystem to your **AWS EC2 Ubuntu 22.04 LTS instance** using **FileZilla (SFTP)** and the automated provisioning script.

---

## 1. Prerequisites
- An active **AWS EC2 instance** running **Ubuntu 22.04 LTS** (e.g. `t3.medium`).
- Your AWS `.pem` private key file.
- **Security Group Inbound Rules** open on EC2:
  - `SSH` (Port 22): Your IP
  - `HTTP` (Port 80): `0.0.0.0/0`
  - `HTTPS` (Port 443): `0.0.0.0/0`
- **DNS Records** pointing to your EC2 Public / Elastic IP:
  - `dbert.in` $\rightarrow$ A record to `YOUR_EC2_IP`
  - `www.dbert.in` $\rightarrow$ CNAME or A record to `YOUR_EC2_IP`
  - `lms.dbert.in` $\rightarrow$ A record to `YOUR_EC2_IP`
  - (Optional for 301 redirects): `dbert.online`, `internship.dbert.online` $\rightarrow$ A records to `YOUR_EC2_IP`

---

## 2. Server Directory Permission Preparation (One-Time via SSH)
Before uploading via FileZilla, connect via SSH terminal (PuTTY or PowerShell SSH):
```bash
ssh -i /path/to/your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```
Create the deployment folder and grant write permissions to user `ubuntu`:
```bash
sudo mkdir -p /var/www/dbert-website-lms
sudo chown -R ubuntu:ubuntu /var/www/dbert-website-lms
```

---

## 3. Upload Codebase via FileZilla (SFTP)

1. Open **FileZilla Client**.
2. Go to **File $\rightarrow$ Site Manager $\rightarrow$ New Site**.
   - **Protocol**: `SFTP - SSH File Transfer Protocol`
   - **Host**: `YOUR_EC2_PUBLIC_IP`
   - **Port**: `22`
   - **Logon Type**: `Key file`
   - **User**: `ubuntu`
   - **Key file**: Click **Browse** and select your `.pem` key file.
3. Click **Connect**.
4. In FileZilla:
   - **Left Window (Local Site)**: Navigate to your local project directory:
     `c:\Users\user\Desktop\dbert-website-lms\`
   - **Right Window (Remote Site)**: Navigate to:
     `/var/www/dbert-website-lms/`
5. Select all files and folders **EXCEPT** (to avoid uploading heavy OS-specific binaries):
   - `node_modules/`
   - `.next/`
   - `.venv/`
   - `cpanel_public_html/`
   - `*.zip`
6. Right-click and select **Upload**.

---

## 4. Run Automated EC2 Provisioning & Deployment

Once FileZilla finishes transferring files, switch to your SSH terminal on EC2:

```bash
cd /var/www/dbert-website-lms

# Configure LMS secrets from sample
cp apps/portal/.env.production.sample apps/portal/.env
nano apps/portal/.env  # (Optional) Verify or change database password & secrets

# Run the all-in-one setup & deployment script
sudo bash deploy/deploy_ec2_unified.sh
```

### What `deploy_ec2_unified.sh` Automatically Does:
1. Verifies/installs system dependencies: Node.js 20 LTS, Python 3.11, PostgreSQL 15, Nginx, and Certbot.
2. Initializes PostgreSQL user `dbert_user` and database `dbert_lms`, applying the database schema.
3. Configures Python virtual environment and installs LMS packages.
4. Compiles Next.js standalone production build for `apps/website`.
5. Installs and starts systemd daemons:
   - `dbert-website.service` on port `3001`
   - `dbert-portal.service` on port `5001`
6. Installs `deploy/dbert-unified-nginx.conf` into `/etc/nginx/sites-available/` and reloads Nginx.
7. Executes automated local health checks on both ports `3001` and `5001`.

---

## 5. Issue Let's Encrypt SSL Certificates via Certbot

Once DNS has propagated and the script completes, issue SSL certificates:
```bash
sudo certbot --nginx -d dbert.in -d www.dbert.in -d lms.dbert.in
```
Follow the interactive prompts (enter email address, agree to Terms). Certbot will automatically configure the SSL certificates in Nginx and set up automatic renewal.

---

## 6. Verification Checklist
- [ ] Visit `https://dbert.in` $\rightarrow$ Homepage loads with styling and typography.
- [ ] Visit `https://lms.dbert.in` $\rightarrow$ LMS dashboard loads with learning-first navigation.
- [ ] Test Course Player: `https://lms.dbert.in/courses`
- [ ] Test 301 redirects: `http://dbert.in` redirects to `https://dbert.in`.
- [ ] Check service statuses:
  ```bash
  sudo systemctl status dbert-website.service
  sudo systemctl status dbert-portal.service
  ```
