"""
routes/masterclass.py - 1-Hour Masterclass Registration & Promotion Blueprint
Live Event: Monday 8:00 PM IST - Remote Data Analyst Internships & Skill Transformation
"""
import os
import re
import csv
import io
import datetime
from flask import Blueprint, render_template, request, jsonify, Response, current_app
from app import get_db, clean_text, now_str, log_error, row_to_dict

masterclass_bp = Blueprint("masterclass", __name__)

# Default community URLs (can be overridden by environment variables or platform_config)
DEFAULT_WHATSAPP_URL = os.environ.get("MASTERCLASS_WHATSAPP_URL", "https://chat.whatsapp.com/invite/DBERTDataAnalystMasterclass")
DEFAULT_DISCORD_URL = os.environ.get("MASTERCLASS_DISCORD_URL", "https://discord.gg/dbert")

def _ensure_masterclass_table(conn):
    """Idempotently create registrations table with proper indexing."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS masterclass_registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            whatsapp TEXT NOT NULL,
            background TEXT,
            current_status TEXT,
            source TEXT DEFAULT 'landing_page',
            ip_address TEXT,
            user_agent TEXT,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        )
    """)
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_mr_email ON masterclass_registrations(email)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_mr_whatsapp ON masterclass_registrations(whatsapp)"
    )


def _get_next_event_datetime():
    """
    Computes the upcoming Monday at 8:00 PM IST (UTC+5:30).
    If today is Monday and time is before 8:00 PM IST, it returns today.
    Otherwise, it returns the following Monday.
    """
    ist = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    now = datetime.datetime.now(ist)
    
    # Days until next Monday: Monday is weekday() == 0
    days_ahead = (0 - now.weekday()) % 7
    if days_ahead == 0 and (now.hour > 20 or (now.hour == 20 and now.minute > 0)):
        days_ahead = 7
    
    next_monday = now + datetime.timedelta(days=days_ahead)
    event_dt = next_monday.replace(hour=20, minute=0, second=0, microsecond=0)
    return event_dt


def _get_community_links(conn):
    """Fetches configured Discord and WhatsApp URLs or returns defaults."""
    whatsapp_url = DEFAULT_WHATSAPP_URL
    discord_url = DEFAULT_DISCORD_URL
    try:
        r_wa = conn.execute("SELECT value FROM platform_config WHERE key='masterclass_whatsapp_url'").fetchone()
        if r_wa and r_wa[0]:
            whatsapp_url = r_wa[0]
        r_dc = conn.execute("SELECT value FROM platform_config WHERE key='masterclass_discord_url'").fetchone()
        if r_dc and r_dc[0]:
            discord_url = r_dc[0]
    except Exception:
        pass
    return whatsapp_url, discord_url


@masterclass_bp.route("/masterclass/data-analyst", methods=["GET"])
def masterclass_landing():
    """Renders the masterclass registration page with live database statistics."""
    with get_db() as conn:
        _ensure_masterclass_table(conn)
        whatsapp_url, discord_url = _get_community_links(conn)

        # 1. Total Remote Indian Data Analyst Internships in DB
        total_remote_query = """
            SELECT COUNT(*) FROM scraped_internships 
            WHERE Region = 'India' AND Is_Remote = 'Yes' 
              AND (Domain LIKE '%Data%' OR Role LIKE '%Data%' OR Role LIKE '%Analyst%' OR Role LIKE '%Analytics%')
        """
        try:
            total_remote = conn.execute(total_remote_query).fetchone()[0]
        except Exception:
            total_remote = 415

        # 2. Sample 8 Featured Verified Openings
        sample_jobs_query = """
            SELECT id, Role, Company, Location, Is_Remote, Stipend, URL, Source
            FROM scraped_internships
            WHERE Region = 'India' AND Is_Remote = 'Yes'
              AND (Domain LIKE '%Data%' OR Role LIKE '%Data%' OR Role LIKE '%Analyst%' OR Role LIKE '%Analytics%')
              AND (LOWER(Stipend) NOT LIKE '%unpaid%' AND Stipend IS NOT NULL AND Stipend != '')
            ORDER BY id DESC LIMIT 8
        """
        sample_jobs = []
        try:
            rows = conn.execute(sample_jobs_query).fetchall()
            for r in rows:
                sample_jobs.append(row_to_dict(r))
        except Exception as e:
            log_error("masterclass_sample_jobs", e)

        # 3. Calculate target event ISO timestamp for client countdown timer
        event_dt = _get_next_event_datetime()
        event_iso = event_dt.isoformat()
        event_display_date = event_dt.strftime("%A, %d %B %Y")

        # 4. Total registrants so far (for social proof)
        try:
            reg_count = conn.execute("SELECT COUNT(*) FROM masterclass_registrations").fetchone()[0]
        except Exception:
            reg_count = 0
        social_proof_registrations = 280 + reg_count

    return render_template(
        "masterclass_data_analyst.html",
        total_remote=total_remote,
        sample_jobs=sample_jobs,
        event_iso=event_iso,
        event_display_date=event_display_date,
        social_proof_count=social_proof_registrations,
        whatsapp_url=whatsapp_url,
        discord_url=discord_url
    )


@masterclass_bp.route("/api/masterclass/register", methods=["POST"])
def masterclass_register_api():
    """Registers an attendee for the free masterclass."""
    data = request.get_json(force=True, silent=True) or {}
    name = clean_text(data.get("name"))
    email = clean_text(data.get("email")).lower()
    whatsapp = clean_text(data.get("whatsapp"))
    background = clean_text(data.get("background"))
    current_status = clean_text(data.get("current_status"))
    source = clean_text(data.get("source")) or "landing_page"

    # Validation
    if not name or len(name) < 2:
        return jsonify({"status": "error", "message": "Please enter your full name."}), 400
    if not email or "@" not in email or "." not in email:
        return jsonify({"status": "error", "message": "Please enter a valid email address."}), 400
    
    # Strip non-digits for phone check
    phone_clean = re.sub(r"\D", "", whatsapp)
    if len(phone_clean) < 10:
        return jsonify({"status": "error", "message": "Please provide a valid 10-digit WhatsApp number."}), 400

    ip_address = request.headers.get("CF-Connecting-IP") or request.headers.get("X-Forwarded-For") or request.remote_addr
    user_agent = request.headers.get("User-Agent", "")[:250]

    with get_db() as conn:
        _ensure_masterclass_table(conn)
        whatsapp_url, discord_url = _get_community_links(conn)

        # Check existing registration
        existing = conn.execute(
            "SELECT id FROM masterclass_registrations WHERE email=? OR whatsapp=?",
            (email, phone_clean)
        ).fetchone()

        if not existing:
            conn.execute("""
                INSERT INTO masterclass_registrations (
                    name, email, whatsapp, background, current_status, source, ip_address, user_agent, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now', 'localtime'))
            """, (name, email, phone_clean, background, current_status, source, ip_address, user_agent))
            conn.commit()

    return jsonify({
        "status": "success",
        "message": "Registration successful! Welcome to the Masterclass.",
        "whatsapp_url": whatsapp_url,
        "discord_url": discord_url,
        "attendee_name": name
    })


@masterclass_bp.route("/admin/masterclass/registrations", methods=["GET"])
def admin_masterclass_registrations():
    """Admin endpoint to view registrations or export as CSV."""
    from services.auth_service import AuthService
    with get_db() as conn:
        _ensure_masterclass_table(conn)
        admin_user = AuthService.require_admin(conn)
        if not admin_user:
            return jsonify({"status": "error", "message": "Unauthorized"}), 401

        is_csv = request.args.get("format") == "csv"
        rows = conn.execute("""
            SELECT id, name, email, whatsapp, background, current_status, source, ip_address, created_at
            FROM masterclass_registrations ORDER BY id DESC
        """).fetchall()

        if is_csv:
            si = io.StringIO()
            cw = csv.writer(si)
            cw.writerow(["ID", "Name", "Email", "WhatsApp", "Background", "Current Status", "Source", "IP", "Registered At"])
            for r in rows:
                cw.writerow([r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8]])
            output = si.getvalue()
            return Response(
                output,
                mimetype="text/csv",
                headers={"Content-Disposition": "attachment;filename=masterclass_registrations.csv"}
            )

        data = [row_to_dict(r) for r in rows]
        return jsonify({
            "status": "success",
            "total": len(data),
            "registrations": data
        })
