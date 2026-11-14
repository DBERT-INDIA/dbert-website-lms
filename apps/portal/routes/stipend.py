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
    SITE_ORIGIN, send_password_reset_email, now_str, _ensure_articles_table
)
from services.certificate_service import CertificateService
from services.ai.stipend_evaluator import (
    StipendEvaluator, get_active_gemini_key, probe_gemini_key,
    get_intern_gemini_key, generate_capstone_case_study
)
from services.linkedin_verifier import LinkedInVerifier


@stipend_bp.route("/stipend/tasks", methods=["GET"])
def stipend_tasks():
    """Intern-facing Stipend Milestone Dashboard with 3-step gating."""
    intern = current_intern()
    if not intern:
        req_email = clean_text(request.args.get("email", "")).lower()
        if req_email:
            reg = CertificateService.load_registry_record(email=req_email)
            if reg:
                flash(f"Welcome {reg.get('holderName', 'Candidate')}! Your certified record is verified. Please sign in or set your password to access your stipend dashboard.", "info")
        return redirect("/#signin")

    email = intern.get("email", "").strip().lower()
    intern_id = intern.get("id")

    with get_db() as conn:
        # 1. Gate 1: Certificate Verification
        ver_info = CertificateService.is_intern_verified(conn, intern_id=intern_id, email=email)
        
        # 2. Gate 2: Completion Date Check
        comp_info = CertificateService.get_intern_completion_info(conn, intern_id=intern_id, email=email)

        # 3. Gate 3: Payout UPI Account Check
        acct = conn.execute("SELECT * FROM intern_accounts WHERE id=?", (intern_id,)).fetchone()
        has_upi = bool(acct and acct["upi_id_encrypted"])
        masked_upi = "Active (Encrypted)"
        if has_upi and hasattr(current_app, "decrypt_upi"):
            try:
                dec = current_app.decrypt_upi(acct["upi_id_encrypted"])
                masked_upi = mask_upi(dec)
            except Exception:
                pass

        # Check Gemini Key status (intern-specific first)
        intern_gemini_key = get_intern_gemini_key(conn, intern_id)
        has_intern_gemini_key = bool(intern_gemini_key)
        intern_gemini_key_masked = ""
        if has_intern_gemini_key:
            if hasattr(current_app, "mask_gemini_key"):
                intern_gemini_key_masked = current_app.mask_gemini_key(intern_gemini_key)
            else:
                intern_gemini_key_masked = intern_gemini_key[:6] + "..." + intern_gemini_key[-4:]

        active_key = intern_gemini_key or get_active_gemini_key(conn, intern_id=intern_id)
        has_gemini = bool(active_key)

        all_gates_passed = bool(ver_info.get("verified") and comp_info.get("is_completed") and has_upi)

        # Fetch domain task
        target_domain = (acct["domain"] if acct and acct["domain"] else ver_info.get("domain", "")).strip()

        # LinkedIn Profile & Experience Verification metadata
        has_linkedin = bool(acct and acct.get("linkedin_url"))
        linkedin_verified = bool(acct and acct.get("linkedin_verified"))
        linkedin_url = acct.get("linkedin_url") or "" if acct else ""
        linkedin_status = acct.get("linkedin_verification_status") or "UNVERIFIED" if acct else "UNVERIFIED"
        cert_val_raw = ver_info.get("cert_id") or ver_info.get("certId") or ""
        add_to_linkedin_url = LinkedInVerifier.build_add_to_linkedin_url(
            target_domain or "AI Engineering", cert_val_raw
        )
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
        capstone_article = None
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

            if existing_submission:
                cert_val = ver_info.get("cert_id") or ver_info.get("certId") or ""
                capstone_article = conn.execute(
                    """
                    SELECT * FROM intern_articles 
                    WHERE intern_id = ? AND (task_submission_id = ? OR (cert_id IS NOT NULL AND cert_id = ? AND cert_id != ''))
                    ORDER BY id DESC LIMIT 1
                    """,
                    (intern_id, existing_submission["id"], cert_val)
                ).fetchone()

    return render_template(
        "stipend_tasks.html",
        intern=intern,
        ver_info=ver_info,
        comp_info=comp_info,
        has_upi=has_upi,
        masked_upi=masked_upi,
        has_gemini=has_gemini,
        has_intern_gemini_key=has_intern_gemini_key,
        intern_gemini_key_masked=intern_gemini_key_masked,
        all_gates_passed=all_gates_passed,
        active_task=active_task,
        existing_submission=existing_submission,
        capstone_article=capstone_article,
        has_linkedin=has_linkedin,
        linkedin_verified=linkedin_verified,
        linkedin_url=linkedin_url,
        linkedin_status=linkedin_status,
        add_to_linkedin_url=add_to_linkedin_url
    )


@stipend_bp.route("/stipend/tasks/<int:task_id>/submit", methods=["POST"])
def submit_stipend_task(task_id: int):
    """Handles intern submission for stipend milestone with AI pre-screening."""
    intern = current_intern()
    if not intern:
        if not request.is_json:
            flash("Please sign in to submit capstone deliverables.", "danger")
            return redirect("/stipend/tasks")
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    intern_id = intern["id"]
    email = intern.get("email", "").strip().lower()

    with get_db() as conn:
        # Pre-flight Gating re-check
        ver_info = CertificateService.is_intern_verified(conn, intern_id=intern_id, email=email)
        if not ver_info.get("verified"):
            if not request.is_json:
                flash("Certificate verification required to submit capstone deliverables.", "danger")
                return redirect("/stipend/tasks")
            return jsonify({"status": "error", "message": "Certificate verification required."}), 403

        comp_info = CertificateService.get_intern_completion_info(conn, intern_id=intern_id, email=email)
        if not comp_info.get("is_completed"):
            if not request.is_json:
                flash("Internship duration has not concluded yet.", "danger")
                return redirect("/stipend/tasks")
            return jsonify({"status": "error", "message": "Internship duration has not concluded yet."}), 403

        acct = conn.execute("SELECT upi_id_encrypted, name, domain FROM intern_accounts WHERE id=?", (intern_id,)).fetchone()
        if not acct or not acct["upi_id_encrypted"]:
            if not request.is_json:
                flash("Please link your verified UPI ID before submitting.", "danger")
                return redirect("/stipend/tasks")
            return jsonify({"status": "error", "message": "Please add your UPI ID before submitting."}), 400

        # Check AI Engine Availability (Prioritizes intern-provided key, fallback to platform key)
        active_key = get_active_gemini_key(conn, intern_id=intern_id)

        task = conn.execute("SELECT * FROM tasks WHERE id = ? AND task_type = 'stipend_milestone'", (task_id,)).fetchone()
        if not task:
            if not request.is_json:
                flash("Task not found.", "danger")
                return redirect("/stipend/tasks")
            return jsonify({"status": "error", "message": "Task not found."}), 404

        # Idempotency Guard: Check for existing active submission
        existing_sub = conn.execute(
            """
            SELECT id, status FROM task_submissions 
            WHERE intern_id = ? AND task_id = ? AND task_category = 'stipend_milestone'
              AND status IN ('pending', 'approved')
            ORDER BY id DESC LIMIT 1
            """,
            (intern_id, task_id)
        ).fetchone()
        if existing_sub:
            if not request.is_json:
                flash("You already have an active submission pending review for this milestone.", "info")
                return redirect("/stipend/tasks")
            return jsonify({
                "status": "success",
                "message": "Submission already active.",
                "submission_id": existing_sub["id"],
                "already_submitted": True
            }), 200

        # Read form inputs
        github_repo_url = clean_text(request.form.get("github_repo_url", ""))
        live_demo_url = clean_text(request.form.get("live_demo_url", ""))
        submission_content = clean_text(request.form.get("submission_content", ""))

        if not github_repo_url:
            if not request.is_json:
                flash("GitHub repository URL is required.", "danger")
                return redirect("/stipend/tasks")
            return jsonify({"status": "error", "message": "GitHub repository URL is required."}), 400
        if not submission_content:
            if not request.is_json:
                flash("Project architecture description is required.", "danger")
                return redirect("/stipend/tasks")
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

        # Execute Automated AI Pre-Screening or Graceful Fallback
        submission_data = {
            "holder_name": acct["name"] if acct else "Intern",
            "github_repo_url": github_repo_url,
            "live_demo_url": live_demo_url,
            "report_file_url": report_file_url,
            "submission_content": submission_content
        }
        domain = (task["target_domain"] or ver_info.get("domain") or "Full Stack Web Development").strip()

        if active_key:
            try:
                eval_result = StipendEvaluator.evaluate(submission_data, domain=domain, api_key=active_key)
                score = eval_result.get("score")
                notes = eval_result.get("notes", "Automated pre-screening complete.")
                eval_status = eval_result.get("verdict", "RECOMMENDED_APPROVE")
            except Exception as e:
                logger.error(f"Error during AI pre-screening for intern {intern_id}: {e}")
                score = None
                notes = "Automated AI evaluation encountered a temporary delay. Queued for mentor staff review."
                eval_status = "AI_FAILED_MANUAL_REVIEW"
        else:
            logger.info(f"AI key not configured; routing submission for intern {intern_id} directly to manual staff review.")
            score = None
            notes = "Submission received and queued for mentor staff review."
            eval_status = "AWAITING_MANUAL_REVIEW"

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

    if eval_status == "AWAITING_MANUAL_REVIEW":
        flash("Your technical contribution was submitted successfully! Mentors will review your project deliverables and release your stipend.", "success")
    else:
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


@stipend_bp.route("/api/intern/gemini-key/save", methods=["POST"])
def intern_gemini_key_save():
    """Validates and saves the intern's own Google Gemini API key with Fernet encryption."""
    intern = current_intern()
    if not intern:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    data = request.json or request.form or {}
    raw_key = (data.get("gemini_api_key") or "").strip()
    if not raw_key:
        return jsonify({"status": "error", "message": "Please enter a valid Gemini API key."}), 400

    # Probe key against Google API
    is_valid, probe_msg = probe_gemini_key(raw_key)
    if not is_valid:
        return jsonify({
            "status": "error",
            "message": f"Google Gemini API key validation failed: {probe_msg}"
        }), 400

    intern_id = intern["id"]
    email = (intern.get("email") or "").strip().lower()

    encrypted_key = None
    if hasattr(current_app, "encrypt_gemini_key"):
        encrypted_key = current_app.encrypt_gemini_key(raw_key)
    else:
        encrypted_key = raw_key

    masked = raw_key[:6] + "..." + raw_key[-4:] if len(raw_key) > 10 else "AIzaSy..."
    if hasattr(current_app, "mask_gemini_key"):
        masked = current_app.mask_gemini_key(raw_key)

    now_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_db() as conn:
        # Multi-account sync for Sakthi
        sakthi_emails = ["sakthi220107@gmail.com", "sakthifriendofgowtham@gmail.com"]
        target_emails = sakthi_emails if email in sakthi_emails else [email]
        for em in target_emails:
            conn.execute(
                """
                UPDATE intern_accounts
                SET gemini_api_key_encrypted = ?, gemini_key_last_verified_at = ?
                WHERE LOWER(email) = LOWER(?)
                """,
                (encrypted_key, now_ts, em)
            )
        conn.commit()

    return jsonify({
        "status": "success",
        "message": "Your Google Gemini API key has been verified and encrypted successfully!",
        "masked_key": masked,
        "probe_details": probe_msg
    })


@stipend_bp.route("/api/intern/gemini-key/status", methods=["GET"])
def intern_gemini_key_status():
    """Returns the configuration status and masked value of the intern's Gemini API key."""
    intern = current_intern()
    if not intern:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    intern_id = intern["id"]
    with get_db() as conn:
        intern_key = get_intern_gemini_key(conn, intern_id)
        if intern_key:
            masked = intern_key[:6] + "..." + intern_key[-4:] if len(intern_key) > 10 else "AIzaSy..."
            if hasattr(current_app, "mask_gemini_key"):
                masked = current_app.mask_gemini_key(intern_key)
            return jsonify({
                "status": "success",
                "has_key": True,
                "masked_key": masked
            })
        return jsonify({
            "status": "success",
            "has_key": False,
            "masked_key": ""
        })


@stipend_bp.route("/intern/articles/scaffold", methods=["POST"])
def intern_articles_scaffold():
    """Auto-generates a rich, structured Capstone Engineering Case Study draft from milestone submission using Gemini."""
    intern = current_intern()
    if not intern:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    intern_id = intern["id"]
    email = (intern.get("email") or "").strip().lower()
    data = request.json or request.form or {}
    force = bool(request.args.get("force") == "true" or data.get("force"))
    inbound_key = (data.get("gemini_api_key") or "").strip()

    with get_db() as conn:
        _ensure_articles_table(conn)

        # 1. Fetch active stipend submission
        sub = conn.execute(
            """
            SELECT s.*, t.title as task_title, t.description as task_desc 
            FROM task_submissions s
            JOIN tasks t ON t.id = s.task_id
            WHERE s.intern_id = ? AND (t.task_type = 'stipend_milestone' OR s.task_category = 'stipend_milestone')
            ORDER BY s.id DESC LIMIT 1
            """,
            (intern_id,)
        ).fetchone()

        if not sub:
            return jsonify({"status": "error", "message": "No active milestone submission found to scaffold from."}), 400

        # Check existing draft
        existing_art = conn.execute(
            "SELECT id, title, status FROM intern_articles WHERE intern_id = ? AND (task_submission_id = ? OR (github_repo_url IS NOT NULL AND github_repo_url = ? AND github_repo_url != ''))",
            (intern_id, sub["id"], sub["github_repo_url"] or "")
        ).fetchone()

        if existing_art and not force:
            return jsonify({
                "status": "success",
                "article_id": existing_art["id"],
                "title": existing_art["title"],
                "article_status": existing_art["status"],
                "redirect_url": f"/intern/articles?edit={existing_art['id']}",
                "already_existed": True,
                "message": "Capstone Case Study draft already exists! Redirecting to editor."
            })

        # 2. Check for active Gemini API key (Strict requirement as per user decision)
        active_gemini_key = None
        if inbound_key:
            # Test and save key immediately
            is_val, val_msg = probe_gemini_key(inbound_key)
            if not is_val:
                return jsonify({"status": "error", "message": f"Provided Gemini key is invalid: {val_msg}"}), 400
            active_gemini_key = inbound_key
            # Save key encrypted
            encrypted_key = current_app.encrypt_gemini_key(inbound_key) if hasattr(current_app, "encrypt_gemini_key") else inbound_key
            now_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn.execute("UPDATE intern_accounts SET gemini_api_key_encrypted = ?, gemini_key_last_verified_at = ? WHERE id = ?",
                         (encrypted_key, now_ts, intern_id))
            conn.commit()
        else:
            active_gemini_key = get_intern_gemini_key(conn, intern_id)

        if not active_gemini_key:
            return jsonify({
                "status": "key_required",
                "message": "A free Google Gemini API key is required to generate your AI Capstone Case Study. Please configure your key."
            }), 400

        # 3. Resolve metadata
        ver_info = CertificateService.is_intern_verified(conn, intern_id=intern_id, email=email)
        cert_id = ver_info.get("cert_id") or ver_info.get("certId") or ""
        author_name = intern.get("name") or ver_info.get("holder_name") or "DBERT Fellow"
        domain = intern.get("domain") or ver_info.get("domain") or "AI & Full Stack Engineering"
        repo_url = (sub.get("github_repo_url") or "").strip()
        demo_url = (sub.get("live_demo_url") or "").strip()
        rubric_score = sub.get("ai_evaluation_score") or 75
        rubric_notes = sub.get("ai_evaluation_notes") or ""

        # Extract project name from repo or title
        project_name = "Capstone Project"
        if repo_url:
            parts = repo_url.rstrip("/").split("/")
            if parts:
                clean_repo = parts[-1].replace(".git", "").replace("-", " ").replace("_", " ").title()
                if clean_repo:
                    project_name = clean_repo
        elif sub.get("task_title"):
            project_name = sub.get("task_title").strip()

        article_title = f"Architecting {project_name}: Production {domain} with DBERT Verified Evaluation"
        now_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        meta = {
            "author_name": author_name,
            "domain": domain,
            "cert_id": cert_id,
            "repo_url": repo_url,
            "demo_url": demo_url,
            "project_name": project_name,
            "rubric_score": rubric_score,
            "rubric_notes": rubric_notes
        }

        # 4. Generate with Gemini
        try:
            md_content = generate_capstone_case_study(meta, active_gemini_key)
        except Exception as ex_gem:
            logger.error(f"[intern_articles_scaffold] Gemini generation error: {ex_gem}")
            return jsonify({
                "status": "error",
                "message": f"Error communicating with Google Gemini API: {str(ex_gem)[:150]}. Please verify your Gemini API key."
            }), 502

        # 5. Insert or Update intern_articles (Enforcing 1 intern = 1 article per topic)
        if existing_art and force:
            conn.execute(
                """
                UPDATE intern_articles SET 
                    title = ?, content_markdown = ?, domain = ?, cert_id = ?, 
                    github_repo_url = ?, live_demo_url = ?, rubric_score = ?, updated_at = ?
                WHERE id = ?
                """,
                (article_title, md_content, domain, cert_id, repo_url, demo_url, rubric_score, now_ts, existing_art["id"])
            )
            art_id = existing_art["id"]
        else:
            # Check by title to prevent duplicates
            topic_match = conn.execute(
                "SELECT id, status FROM intern_articles WHERE intern_id = ? AND LOWER(TRIM(title)) = LOWER(?)",
                (intern_id, article_title.strip())
            ).fetchone()
            if topic_match:
                art_id = topic_match["id"]
                conn.execute(
                    """
                    UPDATE intern_articles SET 
                        content_markdown = ?, domain = ?, cert_id = ?, 
                        github_repo_url = ?, live_demo_url = ?, rubric_score = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (md_content, domain, cert_id, repo_url, demo_url, rubric_score, now_ts, art_id)
                )
            else:
                conn.execute(
                    """
                    INSERT INTO intern_articles (
                        intern_id, domain, title, content_markdown, 
                        task_submission_id, cert_id, github_repo_url, live_demo_url, 
                        rubric_score, stipend_status, status, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDING', 'DRAFT', ?, ?)
                    """,
                    (
                        intern_id, domain, article_title, md_content,
                        sub["id"], cert_id, repo_url, demo_url,
                        rubric_score, now_ts, now_ts
                    )
                )
                art_id = conn.execute("SELECT id FROM intern_articles WHERE intern_id = ? ORDER BY id DESC LIMIT 1", (intern_id,)).fetchone()["id"]

        conn.commit()

        return jsonify({
            "status": "success",
            "article_id": art_id,
            "title": article_title,
            "redirect_url": f"/intern/articles?edit={art_id}",
            "message": "AI Capstone Case Study draft generated successfully with Gemini! Opening editor..."
        })


@stipend_bp.route("/intern/linkedin/submit", methods=["POST"])
def intern_linkedin_submit():
    """Validates public LinkedIn profile URL and triggers automated public experience probe."""
    intern = current_intern()
    if not intern:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    data = request.json or request.form or {}
    raw_url = (data.get("linkedin_url") or "").strip()
    is_valid, canonical = LinkedInVerifier.validate_url(raw_url)
    if not is_valid:
        return jsonify({
            "status": "error",
            "message": "Invalid LinkedIn URL format. Must be a valid public profile (e.g. https://www.linkedin.com/in/username)."
        }), 400

    intern_id = intern["id"]
    email = (intern.get("email") or "").strip().lower()

    with get_db() as conn:
        ver_info = CertificateService.is_intern_verified(conn, intern_id=intern_id, email=email)
        cert_id = ver_info.get("cert_id") or ver_info.get("certId") or ""

        # Probe public profile
        probe_res = LinkedInVerifier.probe_public_profile(canonical, cert_id=cert_id)
        now_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Account syncing for Sakthi or multi-account candidates
        sakthi_emails = ["sakthi220107@gmail.com", "sakthifriendofgowtham@gmail.com"]
        target_emails = sakthi_emails if email in sakthi_emails else [email]

        for em in target_emails:
            if probe_res.get("verified"):
                conn.execute(
                    """
                    UPDATE intern_accounts 
                    SET linkedin_url=?, linkedin_verified=1, linkedin_verified_at=?, 
                        linkedin_last_checked_at=?, linkedin_verification_status='VERIFIED'
                    WHERE LOWER(email)=LOWER(?)
                    """,
                    (canonical, now_ts, now_ts, em)
                )
            elif probe_res.get("status") == "PENDING_SCRAPE":
                conn.execute(
                    """
                    UPDATE intern_accounts 
                    SET linkedin_url=?, linkedin_verified=0, 
                        linkedin_last_checked_at=?, linkedin_verification_status='PENDING_SCRAPE'
                    WHERE LOWER(email)=LOWER(?)
                    """,
                    (canonical, now_ts, em)
                )
            else:
                conn.execute(
                    """
                    UPDATE intern_accounts 
                    SET linkedin_url=?, linkedin_verified=0, 
                        linkedin_last_checked_at=?, linkedin_verification_status='UNVERIFIED'
                    WHERE LOWER(email)=LOWER(?)
                    """,
                    (canonical, now_ts, em)
                )
        conn.commit()

    return jsonify({
        "status": "success",
        "verified": bool(probe_res.get("verified")),
        "verification_status": probe_res.get("status"),
        "canonical_url": canonical,
        "message": probe_res.get("message") or "LinkedIn profile linked successfully! Queued for public credential verification scan."
    })


@stipend_bp.route("/intern/linkedin/check-now", methods=["POST"])
def intern_linkedin_check_now():
    """Forces an immediate re-probe of the intern's public LinkedIn profile."""
    intern = current_intern()
    if not intern:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    intern_id = intern["id"]
    email = (intern.get("email") or "").strip().lower()

    with get_db() as conn:
        acct = conn.execute("SELECT linkedin_url FROM intern_accounts WHERE id=?", (intern_id,)).fetchone()
        if not acct or not acct["linkedin_url"]:
            return jsonify({"status": "error", "message": "No LinkedIn URL linked yet."}), 400

        ver_info = CertificateService.is_intern_verified(conn, intern_id=intern_id, email=email)
        cert_id = ver_info.get("cert_id") or ver_info.get("certId") or ""

        probe_res = LinkedInVerifier.probe_public_profile(acct["linkedin_url"], cert_id=cert_id)
        now_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if probe_res.get("verified"):
            conn.execute(
                """
                UPDATE intern_accounts 
                SET linkedin_verified=1, linkedin_verified_at=?, 
                    linkedin_last_checked_at=?, linkedin_verification_status='VERIFIED'
                WHERE id=?
                """,
                (now_ts, now_ts, intern_id)
            )
        elif probe_res.get("status") == "PENDING_SCRAPE":
            conn.execute(
                """
                UPDATE intern_accounts 
                SET linkedin_last_checked_at=?, linkedin_verification_status='PENDING_SCRAPE'
                WHERE id=?
                """,
                (now_ts, intern_id)
            )
        else:
            conn.execute(
                """
                UPDATE intern_accounts 
                SET linkedin_verified=0, linkedin_last_checked_at=?, linkedin_verification_status='UNVERIFIED'
                WHERE id=?
                """,
                (now_ts, intern_id)
            )
        conn.commit()

    return jsonify({
        "status": "success",
        "verified": bool(probe_res.get("verified")),
        "verification_status": probe_res.get("status"),
        "message": probe_res.get("message")
    })