from typing import Dict, Any, Tuple
from datetime import datetime, timedelta
import logging

def get_week_bounds() -> Tuple[datetime, datetime]:
    now = datetime.now()
    start = now - timedelta(days=now.weekday() + 1) if now.weekday() != 6 else now
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=6, hours=23, minutes=59, seconds=59)
    return start, end

def make_result(status: str, data: Any = None, code: str = None) -> Dict[str, Any]:
    return {
        "status": status,
        "data": data,
        "code": code,
        "request_id": None
    }

class AttendanceService:
    @staticmethod
    def get_summary(conn, intern_id: int, email: str) -> Dict[str, Any]:
        try:
            week_start, _ = get_week_bounds()
            ws = week_start.strftime("%Y-%m-%d")
            row = conn.execute(
                "SELECT total_minutes FROM attendance WHERE (intern_id=? OR (email IS NOT NULL AND LOWER(email)=LOWER(?))) AND week_start=?",
                (intern_id, email, ws)
            ).fetchone()
            mins = row["total_minutes"] if row else 0
            return make_result("ok", {
                "total_minutes": mins,
                "hours": round(mins / 60.0, 1),
                "target_hours": 10,
                "target_minutes": 600,
                "pct": min(100, int(round((mins / 600.0) * 100))),
                "status": "On Track" if mins >= 300 else "Action Needed"
            })
        except Exception as e:
            logging.error(f"AttendanceService failed: {e}")
            return make_result("error", None, "ATTENDANCE_QUERY_FAILED")

class TaskSummaryService:
    @staticmethod
    def get_summary(conn, intern_id: int, email: str) -> Dict[str, Any]:
        try:
            row = conn.execute(
                "SELECT COUNT(*) as count FROM task_submissions WHERE (intern_id=? OR (email IS NOT NULL AND LOWER(email)=LOWER(?))) AND status='approved'",
                (intern_id, email)
            ).fetchone()
            return make_result("ok", row["count"] if row else 0)
        except Exception as e:
            logging.error(f"TaskSummaryService failed: {e}")
            return make_result("error", 0, "TASKS_QUERY_FAILED")

class ApplicationSummaryService:
    @staticmethod
    def get_job_applications(conn, intern_id: int, email: str) -> Dict[str, Any]:
        try:
            job_apps = conn.execute(
                "SELECT pa.id, pa.post_id, pa.status, pa.created_at, pa.decision_note, "
                "p.title AS post_title, p.domain AS post_domain, co.name AS company_name, "
                "p.post_type AS post_type, p.status AS post_status, "
                "d.status AS deposit_status "
                "FROM post_applications pa JOIN posts p ON p.id = pa.post_id "
                "JOIN companies co ON co.id = p.company_id "
                "LEFT JOIN post_hire_deposits d ON d.post_application_id = pa.id "
                "AND d.id = (SELECT MAX(id) FROM post_hire_deposits WHERE post_application_id = pa.id) "
                "WHERE (pa.intern_id = ? OR (pa.email IS NOT NULL AND LOWER(pa.email) = LOWER(?))) ORDER BY pa.id DESC",
                (intern_id, email)
            ).fetchall()
            return make_result("ok", [dict(r) for r in job_apps])
        except Exception as e:
            logging.error(f"ApplicationSummaryService failed: {e}")
            return make_result("error", [], "JOB_APPS_QUERY_FAILED")
