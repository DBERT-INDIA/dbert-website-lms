#!/bin/bash
set -e

echo "=== STEP 1: Creating safety backup on EC2 ==="
tar --exclude='*/node_modules*' --exclude='*/.venv*' --exclude='*/.next*' -czf /home/ubuntu/pre_cleanup_ec2_20261113.tar.gz -C /var/www dbert-website-lms
ls -lh /home/ubuntu/pre_cleanup_ec2_20261113.tar.gz

cd /var/www/dbert-website-lms

echo "=== STEP 2: Creating organized docs directories ==="
mkdir -p docs/audit docs/presentations docs/reports docs/samples

echo "=== STEP 3: Moving audit docs on EC2 ==="
for f in AUDIT_AND_FIX_REPORT.md DBERT_LMS_MASTER_DEVELOPMENT_HARDENING_PLAN.md DBERT_PLATFORM_EVOLUTION_ROADMAP.md DBERT_PLATFORM_QA_AUDIT_AND_PHASED_DEVELOPMENT_PLAN_2026-11-10.md DBERT_Website_LMS_Phase_by_Phase_Fix_Plan.md DBERT_WEBSITE_UIUX_REDESIGN_PHASE_PLAN.md DEVELOPMENT_PROGRESS.md DOMAIN_MIGRATION_AND_GA4_CHANGELOG.md FAILED_FIXES_HANDOVER.md JUSTIFICATION.md ORIGINAL_REQUEST.md QA_REPORT.md WEBSITE_BUG_REGISTER.md WEBSITE_CONTENT_HIERARCHY_AUDIT.md WEBSITE_DESIGN_SYSTEM_AUDIT.md WEBSITE_ROUTE_INVENTORY.md WEBSITE_UIUX_PHASE_PLAN.md WEBSITE_UIUX_PRODUCTION_PREFLIGHT.md WEBSITE_UIUX_PROGRESS.md; do
  [ -f "$f" ] && mv "$f" docs/audit/
done

[ -f "masterclass_remote_data_analyst.pptx" ] && mv "masterclass_remote_data_analyst.pptx" docs/presentations/

echo "=== STEP 4: Removing Windows .bat files and root DBs/scripts from EC2 ==="
rm -f *.bat
rm -f *.db
rm -f route-audit-output.json
rm -f build_cpanel_website_zip.py check_db.py consolidate_internships.py diag.py fetch_jobs.py fetch_more_jobs.py fix_fks.py heal_route.py scrape_apis.py scrape_google.py scrape_indeed_internships.py scrape_indian_internships.py scrape_internships.py scrape_linkedin.py scrape_unstop_internships.py test_ui.py

echo "=== STEP 5: Cleaning apps/website on EC2 ==="
rm -rf apps/website/cpanel-build apps/website/out apps/website/about apps/website/verify apps/website/learners apps/website/pricing apps/website/blog apps/website/cohorts apps/website/hire apps/website/labs apps/website/privacy apps/website/refund apps/website/startups apps/website/terms apps/website/404 apps/website/_next apps/website/ai-consultant apps/website/ai-solutions apps/website/assets apps/website/_not-found

echo "=== STEP 6: Cleaning apps/portal on EC2 ==="
rm -rf apps/portal/vendor apps/portal/cgi-bin apps/portal/flask apps/portal/werkzeug apps/portal/certifi apps/portal/dotenv apps/portal/idna apps/portal/itsdangerous apps/portal/jinja2 apps/portal/jwt apps/portal/markupsafe apps/portal/requests apps/portal/urllib3 apps/portal/*.dist-info apps/portal/backups apps/portal/*.bak*

echo "=== STEP 7: Cleaning data/ on EC2 ==="
rm -f data/scraped_sync_payload.json
rm -f data/*.png

echo "=== STEP 8: Cleaning .agents/teamwork on EC2 ==="
rm -rf .agents/teamwork

echo "=== STEP 9: Cleaning scripts ad-hoc on EC2 ==="
# Retain canonical scripts list
mkdir -p /tmp/canonical_scripts
CANONICAL="deploy_website_updates_to_ec2.py deploy_enrollment_1999_to_ec2.py deploy_directory_to_ec2.py deploy_new_certificates_to_ec2.py deploy_stipend_system_to_ec2.py deploy_bhargavi_approval_to_ec2.py deploy_footer_and_verify_notice.py deploy_sitemap_and_jobs_to_ec2.py full_production_deployment.py fast_sync_to_ec2.py dispatch_409_provisional.py dispatch_9_verified_certificates.py dispatch_cohort_drive_nov2026.py dispatch_sheet_1593.py dispatch_sheet_859_cohort.py quota_watchdog_and_dispatcher.py dbert_inbox_responder.py send_dbert_whatsapp.py verify_and_launch_dbert_whatsapp.py send_ambassador_whatsapp.py send_rejected_payments_whatsapp.py verify_and_launch_16nov_whatsapp.py generate_provisional_registry.py issue_9_verified_certificates.py generate_all_packets.py generate_sample_packet.py sync_verified_certificates_to_portal.py migrate_stipend_schema_and_tasks.py migrate_mentor_group_capacity.py seed_mentor_slots.py run_omnichannel_job_scraper.py verify_production_live.py verify_admin_routes_live.py verify_stipend_flow_e2e.py verify_ec2_deployment.py production_preflight.sh"

for s in $CANONICAL; do
  [ -f "scripts/$s" ] && cp "scripts/$s" /tmp/canonical_scripts/
done

# Remove non-canonical scripts
find scripts -maxdepth 1 -name "*.py" -delete
cp /tmp/canonical_scripts/* scripts/ 2>/dev/null || true
rm -rf /tmp/canonical_scripts
rm -rf scripts/sig_previews scripts/sig_tests scripts/test_stamps scripts/__pycache__

echo "=== STEP 10: Restarting Services and Verifying Health ==="
sudo systemctl restart dbert-portal.service dbert-api.service dbert-website.service nginx.service
sleep 3
systemctl is-active dbert-website.service dbert-portal.service dbert-api.service nginx.service

echo "=== EC2 CLEANUP COMPLETED SUCCESSFULLY ==="
