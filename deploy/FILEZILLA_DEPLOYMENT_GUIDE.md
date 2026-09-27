# DBERT LMS — FileZilla SFTP Deployment & Transition Guide

This guide is tailored for deploying the DBERT LMS platform to your existing AWS EC2 instance using **FileZilla (SFTP)** without disrupting currently running applications.

---

## 1. FileZilla SFTP Connection Setup

1. Open **FileZilla**.
2. Go to **File $\rightarrow$ Site Manager $\rightarrow$ New Site**.
3. Configure the fields:
   - **Protocol:** `SFTP - SSH File Transfer Protocol`
   - **Host:** `YOUR_EC2_PUBLIC_IP` (or domain name)
   - **Port:** `22`
   - **Logon Type:** `Key file`
   - **User:** `ubuntu` (or `ec2-user`)
   - **Key file:** Browse and select your AWS `.pem` private key file.
4. Click **Connect**.

---

## 2. Setting Server Directory Permissions (One-Time via SSH)

Before uploading via FileZilla, prepare the deployment directory permission on EC2:

Connect via SSH terminal (PuTTY or Terminal):
```bash
sudo mkdir -p /var/www/dbert-website-lms
sudo chown -R ec2-user:ec2-user /var/www/dbert-website-lms
```
*(This grants FileZilla write access for `ec2-user` on Amazon Linux 2023 without needing root privileges).*

---

## 3. Uploading Codebase via FileZilla

In FileZilla:
1. **Left Window (Local Site):** Navigate to your local project folder:
   `c:\Users\user\Desktop\dbert-website-lms\`
2. **Right Window (Remote Site):** Navigate to:
   `/var/www/dbert-website-lms/`
3. Select all local files and folders **EXCEPT**:
   - `node_modules/` (Will be installed cleanly on server)
   - `.next/` (Will be built cleanly on server)
   - `.venv/` (Will be built cleanly on server)
4. Right-click and select **Upload**.

---

## 4. EC2 Execution & Switchover Steps (Terminal)

Once FileZilla finishes uploading:

### A. Environment Configuration
Create the production environment file in FileZilla at `/var/www/dbert-website-lms/apps/portal/.env`:
```ini
REQUIRE_POSTGRES=true
DATABASE_URL=postgresql://dbert_user:YOUR_STRONG_PASSWORD@localhost:5432/dbert_lms
SECRET_KEY=your_secure_random_secret_key
CRON_SECRET=your_secure_cron_secret
EMAIL_PROVIDER=cpanel_api
MAILER_URL=https://mailer.aivaratech.online/send
RAZORPAY_KEY_ID=your_razorpay_key
RAZORPAY_KEY_SECRET=your_razorpay_secret
```

### B. Run Automated Build & Health Check Script
Run the automated deployment script over SSH terminal:
```bash
cd /var/www/dbert-website-lms
sudo bash deploy/deploy_ec2.sh
```

---

## 5. FileZilla Upload Rules & Exclusions

To avoid uploading heavy local operating system builds or corrupted virtual environments, add these FileZilla filters (**View $\rightarrow$ Directory comparison / Filename filters**):

- `node_modules`
- `.venv`
- `.next`
- `__pycache__`
- `.pytest_cache`
- `internship.db`
