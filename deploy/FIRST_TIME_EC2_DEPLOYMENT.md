# DBERT LMS — First-Time EC2 Deployment Guide

This guide provides step-by-step instructions for a first-time EC2 deployment of the DBERT LMS platform on Ubuntu 22.04 LTS.

---

## 1. Prerequisites & EC2 Launch Configuration

### EC2 Instance Settings
- **AMI:** Ubuntu 22.04 LTS (64-bit x86)
- **Instance Type:** `t3.medium` (minimum 2 vCPU, 4GB RAM)
- **Storage:** 20 GB GP3 SSD
- **Security Group Inbound Rules:**
  - `SSH` (Port 22): My IP / Admin IP
  - `HTTP` (Port 80): `0.0.0.0/0`
  - `HTTPS` (Port 443): `0.0.0.0/0`

---

## 2. Initial EC2 Server Setup

Connect to your EC2 instance via SSH:
```bash
ssh -i /path/to/your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

Run basic package updates and install system dependencies:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3 python3-venv python3-pip postgresql postgresql-contrib nginx certbot python3-certbot-nginx curl Node.js npm
```

Ensure Node.js 18+ or 20+ LTS is installed:
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

---

## 3. Database Setup (PostgreSQL)

Set up the PostgreSQL user and database:
```bash
sudo -u postgres psql -c "CREATE USER dbert_user WITH PASSWORD 'DBERT_SECURE_PASSWORD_123';"
sudo -u postgres psql -c "CREATE DATABASE dbert_lms OWNER dbert_user;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE dbert_lms TO dbert_user;"
```

Apply the initial PostgreSQL DDL schema:
```bash
sudo mkdir -p /var/www/dbert-website-lms
sudo chown -R ubuntu:ubuntu /var/www/dbert-website-lms
git clone https://github.com/DBERT-INDIA/dbert-website-lms.git /var/www/dbert-website-lms
cd /var/www/dbert-website-lms
PGPASSWORD='DBERT_SECURE_PASSWORD_123' psql -h localhost -U dbert_user -d dbert_lms -f docs/POSTGRES_SCHEMA.sql
```

---

## 4. Environment Variables Setup

Create the production `.env` file at `/var/www/dbert-website-lms/apps/portal/.env`:

```bash
cat << 'EOF' > /var/www/dbert-website-lms/apps/portal/.env
REQUIRE_POSTGRES=true
DATABASE_URL=postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms
SECRET_KEY=generate_a_random_secret_string_here
CRON_SECRET=generate_a_cron_secret_string_here
EMAIL_PROVIDER=cpanel_api
MAILER_URL=https://mailer.aivaratech.online/send
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
EOF
```

---

## 5. Systemd Daemons Setup

### Portal Flask App Service (`/etc/systemd/system/dbert-portal.service`)
```bash
sudo cat << 'EOF' > /etc/systemd/system/dbert-portal.service
[Unit]
Description=DBERT LMS Flask Portal Application
After=network.target postgresql.service

[Service]
User=ubuntu
WorkingDirectory=/var/www/dbert-website-lms/apps/portal
EnvironmentFile=/var/www/dbert-website-lms/apps/portal/.env
ExecStart=/var/www/dbert-website-lms/apps/portal/.venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

### Next.js Marketing App Service (`/etc/systemd/system/dbert-website.service`)
```bash
sudo cat << 'EOF' > /etc/systemd/system/dbert-website.service
[Unit]
Description=DBERT Next.js Marketing Website
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/var/www/dbert-website-lms/apps/website
ExecStart=/usr/bin/npm start -- -p 3000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

Enable and start services:
```bash
sudo systemctl daemon-reload
sudo systemctl enable dbert-portal
sudo systemctl enable dbert-website
```

---

## 6. Nginx & SSL Setup

Copy the repository Nginx configuration:
```bash
sudo cp /var/www/dbert-website-lms/deploy/nginx.conf /etc/nginx/sites-available/internship.dbert.online
sudo ln -sf /etc/nginx/sites-available/internship.dbert.online /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
```

Obtain SSL certificates via Certbot:
```bash
sudo certbot --nginx -d internship.dbert.online
```

---

## 7. Running First Deployment & Verification

Execute the deployment script:
```bash
cd /var/www/dbert-website-lms
sudo bash deploy/deploy_ec2.sh
```

### Zero-Breakage Checklist
1. `curl http://127.0.0.1:5000/health` returns `{"status": "ok"}`.
2. `https://internship.dbert.online/` loads with valid SSL.
3. Systemd logs are clean (`journalctl -u dbert-portal.service -n 50 --no-pager`).
