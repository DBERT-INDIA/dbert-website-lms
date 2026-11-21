"""
routes/admin.py - Administration Routing Blueprint
Fulfills Phase 23 (Monolith Modularization) of INTERNSHIPPORTAL4_LOCAL_AI_AGENT_MASTER_PLAN.md

Endpoints:
- POST /admin/companies/approve
- POST /admin/companies/suspend
- GET  /admin/telemetry
- GET  /admin/learning-analytics
"""
from datetime import datetime, timezone
from flask import Blueprint, jsonify, request, redirect, render_template
from services.auth_service import AuthService
from services.telemetry_service import get_telemetry_snapshot
from app import (
    get_db, require_admin, require_role, now_str, clean_text
)

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/companies/approve", methods=["POST"])
def admin_company_approve():
    """Approves or unapproves a partner company."""
    with get_db() as conn:
        admin_user = AuthService.require_admin(conn)
    if not admin_user:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    data = request.get_json(force=True, silent=True) or {}
    cid = data.get("company_id")
    approve = 1 if data.get("approve", True) else 0

    with get_db() as conn:
        conn.execute(
            "UPDATE companies SET is_approved=?, updated_at=? WHERE id=?",
            (approve, now_str(), cid)
        )
        conn.commit()
    return jsonify({"status": "success", "is_approved": approve})


@admin_bp.route("/admin/companies/suspend", methods=["POST"])
def admin_company_suspend():
    """Suspends or activates a partner company account."""
    with get_db() as conn:
        admin_user = AuthService.require_admin(conn)
    if not admin_user:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    data = request.get_json(force=True, silent=True) or {}
    cid = data.get("company_id")
    active = 0 if data.get("suspend", True) else 1

    with get_db() as conn:
        conn.execute(
            "UPDATE companies SET is_active=?, updated_at=? WHERE id=?",
            (active, now_str(), cid)
        )
        conn.commit()
    return jsonify({"status": "success", "is_active": active})


@admin_bp.route("/admin/telemetry", methods=["GET"])
def admin_telemetry():
    """Real-time observability and telemetry metrics endpoint."""
    with get_db() as conn:
        admin_user = AuthService.require_admin(conn)
    if not admin_user:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    return jsonify({
        "status": "success",
        "metrics": get_telemetry_snapshot()
    })


@admin_bp.route("/admin/integrity-dashboard", methods=["GET"])
def admin_integrity_dashboard():
    """Platform Data Integrity & Health Analytics dashboard.
    
    Supports dual rendering: returns JSON if requested by client or renders
    the comprehensive admin_integrity_dashboard.html template.
    """
    from services.integrity_service import IntegrityService

    with get_db() as conn:
        admin_user = AuthService.require_admin(conn)
        if not admin_user:
            if request.is_json or request.args.get("format") == "json" or request.headers.get("Accept") == "application/json":
                return jsonify({"status": "error", "message": "Unauthorized"}), 401
            return redirect("/admin/login")

        metrics = IntegrityService.get_platform_metrics(conn)
        anomalies = IntegrityService.get_integrity_anomalies(conn)

    if request.is_json or request.args.get("format") == "json" or request.headers.get("Accept") == "application/json":
        return jsonify({
            "status": "success",
            "metrics": metrics,
            "anomalies": anomalies,
            "timestamp": now_str(),
        })

    return render_template(
        "admin_integrity_dashboard.html",
        metrics=metrics,
        anomalies=anomalies,
        now=now_str(),
    )


@admin_bp.route("/admin/integrity/heal", methods=["POST"])
def admin_integrity_heal():
    """Performs safe self-healing / remediation actions (with dry-run support)."""
    from services.integrity_service import IntegrityService

    with get_db() as conn:
        admin_user = AuthService.require_admin(conn)
        if not admin_user:
            return jsonify({"status": "error", "message": "Unauthorized"}), 401

        data = request.get_json(force=True, silent=True) or {}
        action = clean_text(str(data.get("action", "")))
        dry_run = bool(data.get("dry_run", True))

        report = IntegrityService.heal_anomalies(conn, action=action, dry_run=dry_run)

    return jsonify({
        "status": "success",
        "report": report,
    })


@admin_bp.route("/admin/analytics", methods=["GET"])
def admin_analytics():
    """Universal Traffic, Device, Landing Page & SEO Keyword Intelligence Dashboard."""
    import os, json
    with get_db() as conn:
        admin_user = AuthService.require_admin(conn)
        if not admin_user:
            if request.is_json or request.args.get("format") == "json" or request.headers.get("Accept") == "application/json":
                return jsonify({"status": "error", "message": "Unauthorized"}), 401
            return redirect("/admin/login")

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    traffic_file = os.path.join(base_dir, "data", "traffic_analytics_summary.json")
    seo_file = os.path.join(base_dir, "data", "seo_keyword_intelligence.json")

    traffic_data = {}
    if os.path.exists(traffic_file):
        try:
            with open(traffic_file, "r", encoding="utf-8") as f:
                traffic_data = json.load(f)
        except Exception:
            pass

    seo_data = {}
    if os.path.exists(seo_file):
        try:
            with open(seo_file, "r", encoding="utf-8") as f:
                seo_data = json.load(f)
        except Exception:
            pass

    if request.is_json or request.args.get("format") == "json" or request.headers.get("Accept") == "application/json":
        return jsonify({
            "status": "success",
            "traffic": traffic_data,
            "seo": seo_data,
            "timestamp": now_str(),
        })

    return render_template(
        "admin_analytics.html",
        traffic=traffic_data,
        seo=seo_data,
        now=now_str(),
    )


