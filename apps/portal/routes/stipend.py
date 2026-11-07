"""
routes/stipend.py - Technical Contribution & Stipend Milestone Blueprint.
Fulfills Phase 13 of AGENTS.md / GEMINI.md.
"""
import os
import uuid
import secrets
import hashlib
import logging
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, render_template, request, redirect, flash, session, current_app
from werkzeug.utils import secure_filename

stipend_bp = Blueprint("stipend", __name__)
logger = logging.getLogger("stipend_routes")

from app import (
    get_db, current_intern, is_admin_request, current_staff,
    clean_text, log_error, mask_upi, send_email_async,
    credit_intern_coins, get_coin_balances, set_config, get_config,
    SITE_ORIGIN, send_password_reset_email, now_str
)
from services.certificate_service import CertificateService
from services.ai.stipend_evaluator import (
    StipendEvaluator, get_active_gemini_key, probe_gemini_key
)


@stipend_bp.route("/stipend/tasks", methods=["GET"])
def stipend_tasks():
    """Intern-facing Stipend Milestone Dashboard with 3-step gating."""
    intern = current_intern()
    if not intern:
        req_email = clean_text(request.args.get("email", "")).lower()
        if req_email:
            reg = CertificateService.load_registry_record(email=req_email)
            if reg:
                with get_db() as conn:
                    acct = conn.execute("SELECT id FROM intern_accounts WHERE LOWER(email) = LOWER(?)", (req_email,)).fetchone()
                    if not acct:
                        conn.execute(
                            """
                            INSERT INTO intern_accounts 
                            (name, email, domain, college, is_active, password_set, created_at, updated_at)
                            VALUES (?, ?, ?, ?, 1, 0, datetime('now','localtime'), datetime('now','localtime'))
                            """,
                            (reg.get("holderName", "Intern"), req_email, reg.get("domain", "General"), reg.get("college", ""))
                        )
                        conn.commit()
                flash(f"Welcome {reg.get('holderName', 'Candidate')}! Your certified account is recognized. Please sign in or use 'Forgot Password' to set your credentials and claim your stipend.", "info")
        return redirect("/#signin")

    email = intern.get("email", "").strip().lower()
    intern_id = intern.get("id")

    with get_db() as conn:
        # 1. Gate 1: Certificate Verification
        ver_info = CertificateService.is_intern_verified(conn, intern_id=intern_id, email=email)
        
        # 2. Gate 2: Completion Date Check
        comp_info = CertificateService.get_intern_completion_info(conn, intern_id=intern_id, email=email)

        # 3. Gate 3: Payout UPI Account Check
        acct = conn.execute("SELECT upi_id_encrypted, domain, name FROM intern_accounts WHERE id=?", (intern_id,)).fetchone()
        has_upi = bool(acct and acct["upi_id_encrypted"])
        masked_upi = "Active (Encrypted)"
        if has_upi and hasattr(current_app, "decrypt_upi"):
            try:
                dec = current_app.decrypt_upi(acct["upi_id_encrypted"])
                masked_upi = mask_upi(dec)
            except Exception:
                pass

        # Check Gemini Key status
        active_key = get_active_gemini_key(conn)
        has_gemini = bool(active_key)

        all_gates_passed = bool(ver_info.get("verified") and comp_info.get("is_completed") and has_upi)

        # Fetch domain task
        target_domain = (acct["domain"] if acct and acct["domain"] else ver_info.get("domain", "")).strip()
        active_task = None
        if all_gates_passed:
            active_task = conn.execute(
                """
                SELECT * FROM tasks 
                WHERE task_type = 'stipend_milestone' 
                  AND is_active = 1 
                  AND (LOWER(target_domain) = LOWER(?) OR target_domain = '' OR target_domain IS NULL)
                ORDER BY id ASC LIMIT 1
                """,
                (target_domain,)
            ).fetchone()

            if not active_task:
                active_task = conn.execute(
                    "SELECT * FROM tasks WHERE task_type = 'stipend_milestone' AND is_active = 1 LIMIT 1"
                ).fetchone()

        # Check existing submission
        existing_submission = None
        if all_gates_passed:
            existing_submission = conn.execute(
                """
                SELECT s.*, t.title as task_title 
                FROM task_submissions s
                JOIN tasks t ON t.id = s.task_id
                WHERE s.intern_id = ? AND (t.task_type = 'stipend_milestone' OR s.task_category = 'stipend_milestone')
                ORDER BY s.id DESC LIMIT 1
                """,
                (intern_id,)
            ).fetchone()

    return render_template(
        "stipend_tasks.html",
        intern=intern,
        ver_info=ver_info,
        comp_info=comp_info,
        has_upi=has_upi,
        masked_upi=masked_upi,
        has_gemini=has_gemini,
        all_gates_passed=all_gates_passed,
        active_task=active_task,
        existing_submission=existing_submission
    )


@stipend_bp.route("/stipend/tasks/<int:task_id>/submit", methods=["POST"])
def submit_stipend_task(task_id: int):
    """Handles intern submission for stipend milestone with AI pre-screening."""
    intern = current_intern()
    if not intern:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    intern_id = intern["id"]
    email = intern.get("email", "").strip().lower()

    with get_db() as conn:
        # Pre-flight Gating re-check
        ver_info = CertificateService.is_intern_verified(conn, intern_id=intern_id, email=email)
        if not ver_info.get("verified"):
            return jsonify({"status": "error", "message": "Certificate verification required."}), 403

        comp_info = CertificateService.get_intern_completion_info(conn, intern_id=intern_id, email=email)
        if not comp_info.get("is_completed"):
            return jsonify({"status": "error", "message": "Internship duration has not concluded yet."}), 403

        acct = conn.execute("SELECT upi_id_encrypted, name, domain FROM intern_accounts WHERE id=?", (intern_id,)).fetchone()
        if not acct or not acct["upi_id_encrypted"]:
            return jsonify({"status": "error", "message": "Please add your UPI ID before submitting."}), 400

        # Check AI Engine Availability (Strict Pre-flight to prevent silent fails)
        active_key = get_active_gemini_key(conn)
        if not active_key:
            return jsonify({
                "status": "error",
                "message": "AI pre-screening service is currently unconfigured. Submissions are temporarily paused. Please notify administrator."
            }), 503

        task = conn.execute("SELECT * FROM tasks WHERE id = ? AND task_type = 'stipend_milestone'", (task_id,)).fetchone()
        if not task:
            return jsonify({"status": "error", "message": "Task not found."}), 404

        # Read form inputs
        github_repo_url = clean_text(request.form.get("github_repo_url", ""))
        live_demo_url = clean_text(request.form.get("live_demo_url", ""))
        submission_content = clean_text(request.form.get("submission_content", ""))

        if not github_repo_url:
            return jsonify({"status": "error", "message": "GitHub repository URL is required."}), 400
        if not submission_content:
            return jsonify({"status": "error", "message": "Project architecture description is required."}), 400

        # Handle Report PDF upload
        report_file_url = ""
        report_file = request.files.get("report_pdf")
        if report_file and report_file.filename:
            fname = secure_filename(report_file.filename)
            if fname.lower().endswith(".pdf"):
                upload_dir = os.path.join(os.path.dirname(__file__), "..", "uploads", "stipend")
                os.makedirs(upload_dir, exist_ok=True)
                unique_name = f"stipend_{intern_id}_{uuid.uuid4().hex[:8]}_{fname}"
                save_path = os.path.join(upload_dir, unique_name)
                report_file.save(save_path)
                report_file_url = f"/uploads/stipend/{unique_name}"

        # Execute Automated AI Pre-Screening
        submission_data = {
            "holder_name": acct["name"] if acct else "Intern",
            "github_repo_url": github_repo_url,
            "live_demo_url": live_demo_url,
            "report_file_url": report_file_url,
            "submission_content": submission_content
        }
        domain = (task["target_domain"] or ver_info.get("domain") or "Full Stack Web Development").strip()
        eval_result = StipendEvaluator.evaluate(submission_data, domain=domain, api_key=active_key)

        score = eval_result.get("score", 75)
        notes = eval_result.get("notes", "Automated pre-screening complete.")
        eval_status = eval_result.get("verdict", "RECOMMENDED_APPROVE")

        # Save submission record
        conn.execute(
            """
            INSERT INTO task_submissions (
                intern_id, task_id, task_version_id, submission_content, status,
                submission_file, email, github_repo_url, live_demo_url, report_file_url,
                ai_evaluation_score, ai_evaluation_status, ai_evaluation_notes,
                ai_evaluated_at, task_category, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now','localtime'), 'stipend_milestone', datetime('now','localtime'))
            """,
            (
                intern_id, task_id, 1, submission_content, "pending",
                report_file_url, email, github_repo_url, live_demo_url, report_file_url,
                score, eval_status, notes
            )
        )
        conn.commit()

        # Send confirmation email
        student_name = acct["name"] if acct else "Intern"
        email_html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 12px; background: #ffffff;">
            <div style="text-align: center; margin-bottom: 24px;">
                <h2 style="color: #1e1b4b; margin: 0;">DBERT Academic & Project Admissions</h2>
                <p style="color: #64748b; font-size: 13px; margin-top: 4px;">Internship Stipend Milestone Confirmation</p>
            </div>
            <p>Dear <strong>{student_name}</strong>,</p>
            <p>We have received your technical contribution submission for the <strong>{domain}</strong> capstone track.</p>
            
            <div style="background: #f8fafc; border-left: 4px solid #6366f1; padding: 14px; margin: 20px 0; border-radius: 4px;">
                <p style="margin: 0 0 6px 0; font-size: 13px; color: #334155;"><strong>AI Pre-Screening Status:</strong> <span style="color: #059669; font-weight: bold;">{eval_status}</span></p>
                <p style="margin: 0 0 6px 0; font-size: 13px; color: #334155;"><strong>Evaluator Score:</strong> {score}/100</p>
                <p style="margin: 0; font-size: 12px; color: #64748b;"><em>{notes}</em></p>
            </div>

            <p style="font-size: 13px; color: #475569; line-height: 1.6;">
                Your project has been queued for mentor review. Upon staff sign-off, an official bounty of <strong>5,000 Coins (₹5,000)</strong> will be credited directly to your withdrawable LMS wallet.
            </p>
            <p style="margin-top: 24px; font-size: 13px; color: #64748b;">
                Best regards,<br>
                <strong>DBERT Admissions & Evaluation Board</strong><br>
                <a href="https://dbert.in" style="color: #6366f1;">https://dbert.in</a>
            </p>
        </div>
        """
        try:
            send_email_async(
                to_email=email,
                subject=f"Technical Contribution Received: {domain} Capstone (Score: {score}/100)",
                html_body=email_html,
                name=student_name
            )
        except Exception as e:
            logger.error(f"Failed to send submission email to {email}: {e}")

    flash("Your technical contribution was submitted and pre-screened successfully! Mentors will review and release your stipend.", "success")
    return redirect("/stipend/tasks")


@stipend_bp.route("/stipend/activate", methods=["POST"])
def stipend_activate():
    """1-Click password setup and account activation for verified interns."""
    data = request.get_json(silent=True) or request.form
    email = clean_text(data.get("email", "")).lower()
    if not email:
        return jsonify({"status": "error", "message": "Email is required."}), 400

    reg = CertificateService.load_registry_record(email=email)
    if not reg:
        return jsonify({"status": "error", "message": "No certified candidate found for this email address."}), 404

    with get_db() as conn:
        acct = conn.execute("SELECT * FROM intern_accounts WHERE LOWER(email) = LOWER(?)", (email,)).fetchone()
        if not acct:
            conn.execute(
                """
                INSERT INTO intern_accounts 
                (name, email, domain, college, is_active, password_set, created_at, updated_at)
                VALUES (?, ?, ?, ?, 1, 0, datetime('now','localtime'), datetime('now','localtime'))
                """,
                (reg.get("holderName", "Intern"), email, reg.get("domain", "General"), reg.get("college", ""))
            )
            conn.commit()
            acct = conn.execute("SELECT * FROM intern_accounts WHERE LOWER(email) = LOWER(?)", (email,)).fetchone()

        conn.execute("UPDATE password_resets SET used=1, used_at=? WHERE email=? AND account_type='intern' AND used=0", (now_str(), email))
        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        expires_at = (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")

        conn.execute(
            "INSERT INTO password_resets (account_type, account_id, email, token, expires_at) VALUES (?,?,?,?,?)",
            ("intern", acct["id"], email, token_hash, expires_at)
        )
        conn.commit()

        reset_url = f"{SITE_ORIGIN}/reset?token={token}"
        send_password_reset_email(acct["name"], email, reset_url)

    return jsonify({
        "status": "success",
        "message": f"Password activation link dispatched to {email}."
    })


# ==============================================================================
# ADMIN HEALTH & GUIDANCE ENDPOINTS (Eliminates Silent Fails)
# ==============================================================================

@stipend_bp.route("/admin/api/stipend-health", methods=["GET"])
def admin_stipend_health():
    """Provides real-time health telemetry on GEMINI_API_KEY, FERNET_KEY, and verified candidates."""
    if not is_admin_request():
        return jsonify({"status": "error", "message": "Admin authorization required."}), 403

    with get_db() as conn:
        active_key = get_active_gemini_key(conn)
        gemini_ok, gemini_msg = probe_gemini_key(active_key) if active_key else (False, "GEMINI_API_KEY is not configured.")

        # Check Fernet
        from app import FERNET_KEY
        fernet_ok = bool(FERNET_KEY)

        # Count verified certificates in DB
        verified_count = conn.execute("SELECT COUNT(*) c FROM intern_certificates WHERE tier = 'verified'").fetchone()["c"]

        # Check DB type
        db_type = "PostgreSQL" if os.environ.get("REQUIRE_POSTGRES", "false").lower() == "true" else "SQLite"

    return jsonify({
        "status": "success",
        "gemini": {
            "configured": bool(active_key),
            "healthy": gemini_ok,
            "message": gemini_msg,
            "masked_key": (active_key[:8] + "..." + active_key[-4:]) if active_key and len(active_key) > 12 else "None"
        },
        "fernet": {
            "configured": fernet_ok,
            "message": "Fernet UPI encryption key is active." if fernet_ok else "FERNET_KEY is not configured in .env."
        },
        "database": {
            "connected": True,
            "engine": db_type,
            "verified_certificates_in_db": verified_count
        }
    })


@stipend_bp.route("/admin/api/stipend-health/set-gemini-key", methods=["POST"])
def admin_set_gemini_key():
    """Validates and saves a new GEMINI_API_KEY directly through the admin portal."""
    if not is_admin_request():
        return jsonify({"status": "error", "message": "Admin authorization required."}), 403

    data = request.get_json(silent=True) or request.form
    new_key = clean_text(data.get("api_key", ""))
    if not new_key:
        return jsonify({"status": "error", "message": "API key cannot be empty."}), 400

    # Actively test probe key with Google Gemini
    is_valid, probe_msg = probe_gemini_key(new_key)
    if not is_valid:
        return jsonify({
            "status": "error",
            "message": f"Verification failed: {probe_msg}"
        }), 400

    # Save to platform_config
    with get_db() as conn:
        set_config("gemini_api_key", new_key)
        # Update runtime env
        os.environ["GEMINI_API_KEY"] = new_key

    return jsonify({
        "status": "success",
        "message": "GEMINI_API_KEY verified and saved successfully! AI Pre-screening is now active.",
        "probe_details": probe_msg
    })
