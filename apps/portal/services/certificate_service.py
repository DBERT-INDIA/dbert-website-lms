"""
services/certificate_service.py - Intern Certificate Domain Service
Fulfills Phase 23 (Monolith Modularization) of INTERNSHIPPORTAL4_LOCAL_AI_AGENT_MASTER_PLAN.md

Encapsulates:
1. Canonical certificate ID generation and checksum.
2. Certificate retrieval for authenticated interns and public verification.
3. Certificate issuance and metadata serialization.
4. Certificate verification gating and completion lifecycle validation.
"""
import uuid
import os
import json
import calendar
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any


PROGRAM_COHORT_CERTIFICATE_TIER = "program_cohort_completion"


class CertificateService:
    """Certificate management and verification service."""

    @staticmethod
    def generate_certificate_id(course_id: int, intern_id: int) -> str:
        """Mints unique, human-readable certificate serial ID."""
        rand = uuid.uuid4().hex[:6].upper()
        return f"DBERT-C{course_id}-I{intern_id}-{rand}"

    @staticmethod
    def resolve_registry_path() -> Optional[str]:
        """Resolves the absolute path to certificates_registry.json dynamically across local dev and EC2."""
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        candidates = [
            os.path.join(repo_root, "apps", "website", "src", "data", "certificates_registry.json"),
            os.path.join(repo_root, "data", "certificates_registry.json"),
            "/var/www/dbert-website-lms/apps/website/src/data/certificates_registry.json",
            "/var/www/dbert-website-lms/data/certificates_registry.json",
        ]
        for p in candidates:
            if os.path.isfile(p):
                return p
        return None

    @staticmethod
    def load_registry_record(email: Optional[str] = None, cert_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Finds candidate record in master certificates_registry.json (handles dict or list)."""
        path = CertificateService.resolve_registry_path()
        if not path or not os.path.isfile(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            clean_email = (email or "").strip().lower()
            clean_cert = (cert_id or "").strip().lower()

            if isinstance(data, dict):
                if clean_cert:
                    for k, v in data.items():
                        if k.strip().lower() == clean_cert:
                            return v
                records = data.values()
            elif isinstance(data, list):
                records = data
            else:
                records = []

            for item in records:
                if not isinstance(item, dict):
                    continue
                item_email = (item.get("email") or "").strip().lower()
                item_cert = (item.get("certId") or "").strip().lower()
                if clean_email and item_email == clean_email:
                    return item
                if clean_cert and item_cert == clean_cert:
                    return item
        except Exception:
            return None
        return None

    @staticmethod
    def is_intern_verified(conn, intern_id: Optional[int] = None, email: Optional[str] = None) -> Dict[str, Any]:
        """
        Determines if an intern has an officially VERIFIED certificate.
        Dual-layer verification:
        1. Checks intern_certificates in database.
        2. Auto-healing fallback: checks certificates_registry.json. If verified in registry,
           auto-heals/inserts into database and returns verified.
        """
        clean_email = (email or "").strip().lower()
        if not clean_email and intern_id and conn:
            try:
                acct = conn.execute("SELECT email FROM intern_accounts WHERE id = ?", (intern_id,)).fetchone()
                if acct and acct["email"]:
                    clean_email = acct["email"].strip().lower()
            except Exception:
                pass

        # 1. Primary DB Check
        if conn and (clean_email or intern_id):
            try:
                row = conn.execute(
                    """
                    SELECT id, cert_id, course_title, issued_at, tier, email
                    FROM intern_certificates
                    WHERE (
                        (email IS NOT NULL AND LOWER(email) = LOWER(?))
                        OR (? IS NOT NULL AND intern_id = ?)
                    )
                    AND (tier IS NULL OR tier <> ?)
                    ORDER BY id DESC LIMIT 1
                    """,
                    (clean_email or "", intern_id, intern_id, PROGRAM_COHORT_CERTIFICATE_TIER)
                ).fetchone()
                if row:
                    cert_id = row["cert_id"]
                    reg = CertificateService.load_registry_record(email=clean_email, cert_id=cert_id)
                    if reg:
                        is_prov = bool(reg.get("isProvisional", False))
                        is_ver = bool(reg.get("verified", False) and not is_prov)
                        return {
                            "verified": is_ver,
                            "is_provisional": is_prov,
                            "status": "VERIFIED" if is_ver else ("PROVISIONAL" if is_prov else "UNVERIFIED"),
                            "cert_id": reg.get("certId") or cert_id,
                            "domain": reg.get("domain") or row["course_title"],
                            "holder_name": reg.get("holderName", ""),
                            "source": "database_verified"
                        }
                    else:
                        tier_clean = (row["tier"] or "").strip().lower()
                        is_prov = tier_clean in ("provisional", "pending")
                        is_ver = tier_clean in ("verified", "completed", "dbert_verified", "distinction", "merit")
                        return {
                            "verified": is_ver,
                            "is_provisional": is_prov,
                            "status": "VERIFIED" if is_ver else ("PROVISIONAL" if is_prov else "UNVERIFIED"),
                            "cert_id": cert_id,
                            "domain": row["course_title"],
                            "holder_name": "",
                            "source": "database"
                        }
            except Exception:
                pass

        # 2. Master Registry Lookup (Auto-Healing Fallback)
        reg = CertificateService.load_registry_record(email=clean_email)
        if reg:
            is_prov = bool(reg.get("isProvisional", False))
            is_ver = bool(reg.get("verified", False) and not is_prov)
            cert_id = reg.get("certId", "")
            domain = reg.get("domain", "Internship Certificate")
            issue_date = reg.get("issueDate", datetime.now().strftime("%Y-%m-%d"))

            # Auto-heal cache into DB if verified
            if is_ver and conn:
                try:
                    conn.execute(
                        """
                        INSERT INTO intern_certificates 
                        (intern_id, course_id, course_title, cert_id, issued_at, url, tier, email)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (intern_id or 0, 0, domain, cert_id, issue_date, f"/verify/{cert_id}", "verified", clean_email)
                    )
                    conn.commit()
                except Exception:
                    pass

            return {
                "verified": is_ver,
                "is_provisional": is_prov,
                "status": "VERIFIED" if is_ver else ("PROVISIONAL" if is_prov else "UNVERIFIED"),
                "cert_id": cert_id,
                "domain": domain,
                "holder_name": reg.get("holderName", ""),
                "source": "registry_autohealed" if is_ver else "registry"
            }

        return {
            "verified": False,
            "is_provisional": False,
            "status": "NOT_FOUND",
            "cert_id": "",
            "domain": "",
            "holder_name": "",
            "source": "none"
        }

    @staticmethod
    def parse_flexible_date(date_str: Optional[str]) -> Optional[date]:
        """Parses YYYY-MM-DD or Month Year (e.g. 'September 2026') into date object."""
        if not date_str or not isinstance(date_str, str):
            return None
        clean = date_str.strip()
        try:
            return datetime.strptime(clean, "%Y-%m-%d").date()
        except ValueError:
            pass
        try:
            return datetime.strptime(clean, "%d %B %Y").date()
        except ValueError:
            pass
        for fmt in ("%B %Y", "%b %Y"):
            try:
                dt = datetime.strptime(clean, fmt)
                last_day = calendar.monthrange(dt.year, dt.month)[1]
                return date(dt.year, dt.month, last_day)
            except ValueError:
                pass
        return None

    MIN_STIPEND_PAYOUT_DATE = date(2026, 12, 3)  # Earliest inaugural disbursement date

    @classmethod
    def calculate_payout_release_date(cls, end_date_raw: Any) -> tuple[str, str]:
        """Calculates payout date as strictly 60 days after end date, with a strict floor of 2026-12-03.
        
        Formula: max(end_date + 60 days, 2026-12-03)
        Returns:
            (payout_date_iso, payout_date_display) e.g. ("2026-12-03", "Thursday, 03 December 2026")
        """
        if not end_date_raw:
            return cls.MIN_STIPEND_PAYOUT_DATE.strftime("%Y-%m-%d"), cls.MIN_STIPEND_PAYOUT_DATE.strftime("%A, %d %B %Y")
        
        end_dt = None
        if isinstance(end_date_raw, str):
            end_dt = cls.parse_flexible_date(end_date_raw)
        elif isinstance(end_date_raw, datetime):
            end_dt = end_date_raw.date()
        elif isinstance(end_date_raw, date):
            end_dt = end_date_raw

        if not end_dt:
            return cls.MIN_STIPEND_PAYOUT_DATE.strftime("%Y-%m-%d"), cls.MIN_STIPEND_PAYOUT_DATE.strftime("%A, %d %B %Y")

        raw_payout = end_dt + timedelta(days=60)
        final_payout = max(raw_payout, cls.MIN_STIPEND_PAYOUT_DATE)
        return final_payout.strftime("%Y-%m-%d"), final_payout.strftime("%A, %d %B %Y")

    @staticmethod
    def get_intern_completion_info(conn, intern_id: Optional[int] = None, email: Optional[str] = None) -> Dict[str, Any]:
        """
        Determines the intern's completion date and eligibility.
        Rule: Enrollment Table First (joining_date + 60 days). Fallback: Certificate registry endDate.
        Payout Date Rule: Strictly 60 days after completion date, floored at 2026-12-03.
        """
        clean_email = (email or "").strip().lower()
        if not clean_email and intern_id and conn:
            try:
                acct = conn.execute("SELECT email FROM intern_accounts WHERE id = ?", (intern_id,)).fetchone()
                if acct and acct["email"]:
                    clean_email = acct["email"].strip().lower()
            except Exception:
                pass

        today = date.today()

        # 1. Check Enrollment joining_date
        if conn and (clean_email or intern_id):
            try:
                if not clean_email and intern_id:
                    acct = conn.execute("SELECT email FROM intern_accounts WHERE id = ?", (intern_id,)).fetchone()
                    if acct and acct["email"]:
                        clean_email = acct["email"].strip().lower()

                row = conn.execute(
                    """
                    SELECT joining_date FROM enrollments
                    WHERE email IS NOT NULL AND LOWER(email) = LOWER(?)
                    ORDER BY id DESC LIMIT 1
                    """,
                    (clean_email or "",)
                ).fetchone()
                if row and row["joining_date"]:
                    jd = CertificateService.parse_flexible_date(row["joining_date"])
                    if jd:
                        comp_date = jd + timedelta(days=60)
                        is_comp = today >= comp_date
                        days_rem = max(0, (comp_date - today).days)
                        p_iso, p_disp = CertificateService.calculate_payout_release_date(comp_date)
                        return {
                            "joining_date": jd.strftime("%Y-%m-%d"),
                            "completion_date": comp_date.strftime("%Y-%m-%d"),
                            "completion_date_display": comp_date.strftime("%d %b %Y"),
                            "payout_date": p_iso,
                            "payout_date_display": p_disp,
                            "is_completed": is_comp,
                            "days_remaining": days_rem,
                            "source": "enrollment"
                        }
            except Exception:
                pass

        # 2. Fallback to Certificate Registry
        cert_id = None
        if conn and (clean_email or intern_id):
            try:
                cert_row = conn.execute(
                    """SELECT cert_id FROM intern_certificates WHERE LOWER(email) = LOWER(?)
                       AND (tier IS NULL OR tier <> ?) ORDER BY id DESC LIMIT 1""",
                    (clean_email or "", PROGRAM_COHORT_CERTIFICATE_TIER)
                ).fetchone()
                if cert_row and cert_row["cert_id"]:
                    cert_id = cert_row["cert_id"]
            except Exception:
                pass

        reg = CertificateService.load_registry_record(email=clean_email, cert_id=cert_id)
        if reg:
            end_str = reg.get("endDate")
            start_str = reg.get("startDate")
            cd = CertificateService.parse_flexible_date(end_str)
            jd = CertificateService.parse_flexible_date(start_str)
            if cd:
                is_comp = today >= cd
                days_rem = max(0, (cd - today).days)
                p_iso, p_disp = CertificateService.calculate_payout_release_date(cd)
                return {
                    "joining_date": jd.strftime("%Y-%m-%d") if jd else (cd - timedelta(days=60)).strftime("%Y-%m-%d"),
                    "completion_date": cd.strftime("%Y-%m-%d"),
                    "completion_date_display": cd.strftime("%d %b %Y"),
                    "payout_date": p_iso,
                    "payout_date_display": p_disp,
                    "is_completed": is_comp,
                    "days_remaining": days_rem,
                    "source": "certificate_registry"
                }

        # 3. Fallback to intern_accounts created_at
        if conn and (clean_email or intern_id):
            try:
                acct = conn.execute(
                    "SELECT created_at FROM intern_accounts WHERE (email IS NOT NULL AND LOWER(email) = LOWER(?)) OR id = ? LIMIT 1",
                    (clean_email or "", intern_id or -1)
                ).fetchone()
                if acct and acct["created_at"]:
                    cad = CertificateService.parse_flexible_date(acct["created_at"])
                    if cad:
                        comp_date = cad + timedelta(days=60)
                        is_comp = today >= comp_date
                        days_rem = max(0, (comp_date - today).days)
                        p_iso, p_disp = CertificateService.calculate_payout_release_date(comp_date)
                        return {
                            "joining_date": cad.strftime("%Y-%m-%d"),
                            "completion_date": comp_date.strftime("%Y-%m-%d"),
                            "completion_date_display": comp_date.strftime("%d %b %Y"),
                            "payout_date": p_iso,
                            "payout_date_display": p_disp,
                            "is_completed": is_comp,
                            "days_remaining": days_rem,
                            "source": "account_creation"
                        }
            except Exception:
                pass

        # Default fallback: Strictly fail closed if dates cannot be verified
        p_iso, p_disp = CertificateService.calculate_payout_release_date(None)
        return {
            "joining_date": "",
            "completion_date": "",
            "completion_date_display": "Pending Date Verification",
            "payout_date": p_iso,
            "payout_date_display": p_disp,
            "is_completed": False,
            "days_remaining": None,
            "source": "none",
            "requires_manual_review": True
        }

    @staticmethod
    def get_intern_certificates(conn, intern_id: int, email: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieves earned certificates for a given intern ID or email."""
        rows = conn.execute(
            """
            SELECT id, course_id, course_title, cert_id, issued_at, url, tier, email
            FROM intern_certificates
            WHERE intern_id = ? OR (email IS NOT NULL AND LOWER(email) = LOWER(?))
            ORDER BY id DESC
            """,
            (intern_id, email or "")
        ).fetchall()
        return [dict(r) for r in rows]

    @staticmethod
    def verify_certificate(conn, cert_id: str) -> Optional[Dict[str, Any]]:
        """Public verification lookup for a certificate serial ID."""
        if not cert_id:
            return None
        row = conn.execute(
            """
            SELECT c.id, c.course_id, c.course_title, c.cert_id, c.issued_at, c.url, c.tier,
                   COALESCE(i.name, a.name, 'Student') AS recipient_name
            FROM intern_certificates c
            LEFT JOIN intern_accounts i ON i.id = c.intern_id
            LEFT JOIN applications a ON a.email = c.email
            WHERE LOWER(c.cert_id) = LOWER(?)
            LIMIT 1
            """,
            (cert_id.strip(),)
        ).fetchone()
        return dict(row) if row else None

    @staticmethod
    def issue_certificate(
        conn,
        intern_id: int,
        course_id: int,
        course_title: str,
        email: str,
        tier: str = "completed",
        custom_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Atomically issues a certificate row if not already present."""
        existing = conn.execute(
            """
            SELECT cert_id FROM intern_certificates 
            WHERE (intern_id = ? OR (email IS NOT NULL AND LOWER(email) = LOWER(?)))
              AND course_id = ? AND tier = ?
            LIMIT 1
            """,
            (intern_id, email, course_id, tier)
        ).fetchone()
        if existing:
            return {"cert_id": existing["cert_id"], "already_issued": True}

        cert_id = CertificateService.generate_certificate_id(course_id, intern_id)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        url = custom_url or f"/portal/certificate/{cert_id}"

        conn.execute(
            """
            INSERT INTO intern_certificates 
            (intern_id, course_id, course_title, cert_id, issued_at, url, tier, email)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (intern_id, course_id, course_title, cert_id, now, url, tier, (email or "").lower())
        )
        conn.commit()

        try:
            from services.outbox_service import enqueue_outbox_event, EVENT_CERTIFICATE_ISSUED
            enqueue_outbox_event(
                conn,
                event_type=EVENT_CERTIFICATE_ISSUED,
                aggregate_type="certificate",
                aggregate_id=cert_id,
                payload={"intern_id": intern_id, "course_id": course_id, "cert_id": cert_id, "email": email}
            )
        except Exception:
            pass

        return {
            "cert_id": cert_id,
            "course_title": course_title,
            "issued_at": now,
            "url": url,
            "tier": tier,
            "already_issued": False
        }

    @staticmethod
    def issue_course_completion_certificate(
        conn,
        intern_id: int,
        course_id: int,
        email: Optional[str] = None
    ) -> Dict[str, Any]:
        """Automatically issues a course completion certificate if the course was completed."""
        course = conn.execute("SELECT id, title, domain FROM courses WHERE id = ?", (course_id,)).fetchone()
        if not course:
            return {"error": "Course not found", "already_issued": False}

        if not email:
            acct = conn.execute("SELECT email, name FROM intern_accounts WHERE id = ?", (intern_id,)).fetchone()
            email = acct["email"] if acct else ""

        tier = "course_completion"
        existing = conn.execute(
            """
            SELECT cert_id, url FROM intern_certificates 
            WHERE (intern_id = ? OR (email IS NOT NULL AND LOWER(email) = LOWER(?)))
              AND course_id = ?
            LIMIT 1
            """,
            (intern_id, email or "", course_id)
        ).fetchone()

        if existing:
            return {
                "cert_id": existing["cert_id"],
                "url": existing["url"] or f"/portal/certificate/{existing['cert_id']}",
                "already_issued": True,
                "course_title": course["title"]
            }

        return CertificateService.issue_certificate(
            conn=conn,
            intern_id=intern_id,
            course_id=course_id,
            course_title=course["title"],
            email=email or "",
            tier=tier,
            custom_url=None
        )
