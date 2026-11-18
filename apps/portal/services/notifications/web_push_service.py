"""
services/notifications/web_push_service.py - Sovereign Native VAPID Web Push Engine
Fulfills RFC 8292 NIST P-256 standard with zero third-party vendor dependencies.
Powers real-time browser push notifications across all stages of the user usage lifecycle:
Applications, Offer Letters, Payments/Gates, Courses/Quizzes, Attendance/Login Hours,
Mentor Sessions, Tasks/Bounties, Stipend Milestones, Cohort Kickoffs, and Admin Broadcasts.
"""

import os
import sys
import json
import logging
import threading
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger("web_push_service")

# Auto-detect base directory
PORTAL_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VAPID_DIR = os.path.join(PORTAL_DIR, ".vapid")
os.makedirs(VAPID_DIR, exist_ok=True)

VAPID_PRIVATE_FILE = os.path.join(VAPID_DIR, "private_key.pem")
VAPID_PUBLIC_FILE = os.path.join(VAPID_DIR, "public_key.txt")
VAPID_CLAIM_EMAIL = os.environ.get("VAPID_CLAIM_EMAIL", "mailto:contactus@dbert.in")


class VapidManager:
    """Manages persistent NIST P-256 VAPID key generation and retrieval."""
    _instance = None
    _vapid_obj = None
    _public_key_b64 = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._init_keys()
        return cls._instance

    def _init_keys(self):
        try:
            from py_vapid import Vapid
            from py_vapid.utils import b64urlencode
            from cryptography.hazmat.primitives import serialization

            # Check if key files already exist
            if os.path.exists(VAPID_PRIVATE_FILE) and os.path.exists(VAPID_PUBLIC_FILE):
                with open(VAPID_PRIVATE_FILE, "rb") as f:
                    self._vapid_obj = Vapid.from_pem(f.read())
                with open(VAPID_PUBLIC_FILE, "r", encoding="utf-8") as f:
                    self._public_key_b64 = f.read().strip()
                logger.info("Loaded existing VAPID keypair from disk.")
            else:
                logger.info("Generating new sovereign NIST P-256 VAPID keypair...")
                self._vapid_obj = Vapid()
                self._vapid_obj.generate_keys()

                # Save private key PEM
                with open(VAPID_PRIVATE_FILE, "wb") as f:
                    f.write(self._vapid_obj.private_pem())

                # Generate and save base64url uncompressed public key point
                raw_pub = self._vapid_obj.public_key.public_bytes(
                    serialization.Encoding.X962,
                    serialization.PublicFormat.UncompressedPoint
                )
                self._public_key_b64 = b64urlencode(raw_pub)
                with open(VAPID_PUBLIC_FILE, "w", encoding="utf-8") as f:
                    f.write(self._public_key_b64)

                logger.info(f"VAPID keys successfully generated and stored in {VAPID_DIR}")

        except Exception as e:
            logger.error(f"Failed to initialize VAPID keys: {e}")
            raise

    def get_public_key(self) -> str:
        return self._public_key_b64

    def get_vapid_obj(self):
        return self._vapid_obj


def get_public_vapid_key() -> str:
    """Returns the base64url-encoded VAPID public key for browser pushManager.subscribe()."""
    mgr = VapidManager.get_instance()
    return mgr.get_public_key()


def register_device(
    conn,
    user_email: str,
    endpoint: str,
    p256dh: str,
    auth: str,
    device_name: str,
    device_type: str = "desktop",
    user_agent: str = "",
    ip_address: str = "",
    intern_id: Optional[int] = None
) -> Tuple[bool, str]:
    """
    Registers or updates a client browser push device subscription in web_push_devices.
    Idempotent: updates credentials if the endpoint already exists.
    """
    if not endpoint or not p256dh or not auth:
        return False, "Missing required subscription keys"

    clean_email = (user_email or "").strip().lower()

    # Resolve intern_id from email if not explicitly provided
    if not intern_id and clean_email:
        try:
            acc = conn.execute("SELECT id FROM intern_accounts WHERE LOWER(email) = ?", (clean_email,)).fetchone()
            if acc:
                intern_id = acc["id"]
        except Exception:
            pass

    now_iso = datetime.utcnow().isoformat()

    try:
        existing = conn.execute("SELECT id FROM web_push_devices WHERE endpoint = ?", (endpoint,)).fetchone()
        if existing:
            conn.execute("""
                UPDATE web_push_devices SET
                    user_email = ?,
                    intern_id = COALESCE(?, intern_id),
                    p256dh = ?,
                    auth = ?,
                    device_name = ?,
                    device_type = ?,
                    user_agent = ?,
                    ip_address = ?,
                    is_active = 1,
                    last_seen_at = ?
                WHERE id = ?
            """, (clean_email, intern_id, p256dh, auth, device_name, device_type, user_agent, ip_address, now_iso, existing["id"]))
        else:
            conn.execute("""
                INSERT INTO web_push_devices (
                    intern_id, user_email, endpoint, p256dh, auth,
                    device_name, device_type, user_agent, ip_address,
                    is_active, created_at, last_seen_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
            """, (intern_id, clean_email, endpoint, p256dh, auth, device_name, device_type, user_agent, ip_address, now_iso, now_iso))

        conn.commit()
        return True, "Device successfully registered for push notifications."
    except Exception as e:
        logger.error(f"Error registering web push device: {e}")
        return False, str(e)


def unregister_device(conn, endpoint: str) -> bool:
    """Deactivates a device push subscription."""
    try:
        conn.execute("UPDATE web_push_devices SET is_active = 0 WHERE endpoint = ?", (endpoint,))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"Error unregistering device: {e}")
        return False


def revoke_device_by_id(conn, device_id: int, intern_id: Optional[int] = None, email: Optional[str] = None) -> bool:
    """Revokes a device by ID ensuring user ownership."""
    try:
        if intern_id:
            conn.execute("UPDATE web_push_devices SET is_active = 0 WHERE id = ? AND intern_id = ?", (device_id, intern_id))
        elif email:
            conn.execute("UPDATE web_push_devices SET is_active = 0 WHERE id = ? AND LOWER(user_email) = ?", (device_id, email.lower()))
        else:
            conn.execute("UPDATE web_push_devices SET is_active = 0 WHERE id = ?", (device_id,))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"Error revoking device {device_id}: {e}")
        return False


def get_user_devices(conn, intern_id: Optional[int] = None, email: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns active registered devices for an intern account."""
    clean_email = (email or "").strip().lower()
    try:
        rows = conn.execute("""
            SELECT id, device_name, device_type, ip_address, is_active, preferences,
                   created_at, last_pushed_at, last_seen_at
            FROM web_push_devices
            WHERE (intern_id = ? OR (user_email IS NOT NULL AND LOWER(user_email) = ?))
              AND is_active = 1
            ORDER BY last_seen_at DESC
        """, (intern_id, clean_email)).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        logger.error(f"Error fetching user devices: {e}")
        return []


def update_device_preferences(conn, intern_id: int, preferences: Dict[str, bool]) -> bool:
    """Updates push notification category preferences across all devices of an intern."""
    try:
        pref_json = json.dumps(preferences)
        conn.execute("UPDATE web_push_devices SET preferences = ? WHERE intern_id = ?", (pref_json, intern_id))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"Error updating device preferences: {e}")
        return False


# ──────────────────────────────────────────────────────────────────────────────
# Core Non-Blocking Dispatch Engine with Zero Silent Fails
# ──────────────────────────────────────────────────────────────────────────────

def _log_delivery_telemetry(
    conn,
    event_name: str,
    target_email: str,
    title: str,
    body: str,
    target_url: str,
    status_code: Optional[int],
    delivery_status: str,
    error_message: Optional[str] = None,
    intern_id: Optional[int] = None,
    device_id: Optional[int] = None
):
    """Guarantees zero silent fails by logging every push dispatch attempt into web_push_delivery_logs."""
    try:
        conn.execute("""
            INSERT INTO web_push_delivery_logs (
                event_name, target_email, intern_id, device_id,
                title, body, target_url, status_code, delivery_status, error_message, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event_name, target_email, intern_id, device_id,
            title, body, target_url, status_code, delivery_status,
            error_message, datetime.utcnow().isoformat()
        ))
        conn.commit()
    except Exception as e:
        logger.error(f"Failed to log web push delivery telemetry: {e}")


def dispatch_lifecycle_push(
    event_name: str,
    target_email: Optional[str] = None,
    intern_id: Optional[int] = None,
    title: str = "DBERT Notification",
    body: str = "",
    url: str = "https://lms.dbert.in",
    icon: str = "/static/img/dbert-logo-192.png",
    badge: str = "/static/img/dbert-badge-96.png",
    tag: Optional[str] = None,
    extra_data: Optional[Dict[str, Any]] = None,
    target_cohort: str = "all",
    sync_inapp: bool = True
):
    """
    Asynchronously signs and dispatches a native VAPID web push to all matching devices.
    Eliminates silent fails by auditing all outcomes in web_push_delivery_logs.
    Dual-syncs with in-app notifications inbox.
    """
    def _worker():
        from app import app, get_db
        with app.app_context():
            with get_db() as conn:
                clean_email = (target_email or "").strip().lower()

                # 1. Resolve intern_id & email pairing
                resolved_intern_id = intern_id
                if not resolved_intern_id and clean_email:
                    try:
                        acc = conn.execute("SELECT id FROM intern_accounts WHERE LOWER(email) = ?", (clean_email,)).fetchone()
                        if acc:
                            resolved_intern_id = acc["id"]
                    except Exception:
                        pass

                # 2. Dual In-App Sync (persist into notifications table)
                if sync_inapp and resolved_intern_id:
                    try:
                        conn.execute("""
                            INSERT INTO notifications (intern_id, kind, title, body, link, is_read, created_at)
                            VALUES (?, ?, ?, ?, ?, 0, ?)
                        """, (resolved_intern_id, event_name, title, body, url, datetime.utcnow().isoformat()))
                        conn.commit()
                    except Exception as e:
                        logger.error(f"In-app sync error for {clean_email}: {e}")

                # 3. Retrieve Target Devices
                devices = []
                try:
                    if event_name == "broadcast":
                        if target_cohort == "all":
                            devices = conn.execute("SELECT * FROM web_push_devices WHERE is_active = 1").fetchall()
                        else:
                            # Filter by domain track
                            devices = conn.execute("""
                                SELECT d.* FROM web_push_devices d
                                JOIN intern_accounts i ON i.id = d.intern_id
                                WHERE d.is_active = 1 AND LOWER(i.domain_track) LIKE ?
                            """, (f"%{target_cohort.lower()}%",)).fetchall()
                    else:
                        devices = conn.execute("""
                            SELECT * FROM web_push_devices
                            WHERE (intern_id = ? OR (user_email IS NOT NULL AND LOWER(user_email) = ?))
                              AND is_active = 1
                        """, (resolved_intern_id, clean_email)).fetchall()
                except Exception as e:
                    logger.error(f"Error querying web push devices for {clean_email}: {e}")
                    _log_delivery_telemetry(conn, event_name, clean_email, title, body, url, None, "FAILED", f"DB Query Error: {e}", resolved_intern_id)
                    return

                # If no devices are registered yet
                if not devices:
                    logger.info(f"[{event_name}] No active push devices found for {clean_email or target_cohort}. In-app notification synced.")
                    _log_delivery_telemetry(conn, event_name, clean_email, title, body, url, None, "SKIPPED_NO_DEVICE", "User has not yet registered a browser push device", resolved_intern_id)
                    return

                # 4. Prepare Web Push Payload & Keys
                try:
                    vapid_mgr = VapidManager.get_instance()
                    vapid_obj = vapid_mgr.get_vapid_obj()
                except Exception as e:
                    logger.error(f"VAPID manager uninitialized: {e}")
                    _log_delivery_telemetry(conn, event_name, clean_email, title, body, url, None, "FAILED", f"VAPID Init Error: {e}", resolved_intern_id)
                    return

                from pywebpush import webpush, WebPushException

                push_payload = json.dumps({
                    "title": title,
                    "body": body,
                    "icon": icon,
                    "badge": badge,
                    "tag": tag or f"dbert-{event_name}",
                    "data": {
                        "url": url,
                        "event_name": event_name,
                        **(extra_data or {})
                    }
                })

                now_iso = datetime.utcnow().isoformat()

                # 5. Dispatch to Each Device
                for dev in devices:
                    dev_id = dev["id"]
                    sub_info = {
                        "endpoint": dev["endpoint"],
                        "keys": {
                            "p256dh": dev["p256dh"],
                            "auth": dev["auth"]
                        }
                    }

                    try:
                        resp = webpush(
                            subscription_info=sub_info,
                            data=push_payload,
                            vapid_private_key=vapid_obj,
                            vapid_claims={"sub": VAPID_CLAIM_EMAIL},
                            timeout=8
                        )
                        status_code = resp.status_code if hasattr(resp, "status_code") else 201

                        if 200 <= status_code < 300:
                            conn.execute("UPDATE web_push_devices SET last_pushed_at = ? WHERE id = ?", (now_iso, dev_id))
                            conn.commit()
                            _log_delivery_telemetry(conn, event_name, clean_email, title, body, url, status_code, "DELIVERED", None, resolved_intern_id, dev_id)
                            logger.info(f"✓ Push [{event_name}] DELIVERED to device {dev_id} ({dev['device_name']}) for {clean_email}")
                        else:
                            _log_delivery_telemetry(conn, event_name, clean_email, title, body, url, status_code, "FAILED", getattr(resp, "text", ""), resolved_intern_id, dev_id)

                    except WebPushException as ex:
                        status_code = getattr(ex.response, "status_code", 500) if getattr(ex, "response", None) is not None else 500
                        err_text = str(ex)

                        # Prune expired subscriptions (404 Not Found or 410 Gone)
                        if status_code in (404, 410) or "410 Gone" in err_text or "404 Not Found" in err_text:
                            conn.execute("UPDATE web_push_devices SET is_active = 0 WHERE id = ?", (dev_id,))
                            conn.commit()
                            _log_delivery_telemetry(conn, event_name, clean_email, title, body, url, status_code, "EXPIRED_PRUNED", err_text, resolved_intern_id, dev_id)
                            logger.info(f"Pruned expired device {dev_id} (Status: {status_code}) for {clean_email}")
                        else:
                            _log_delivery_telemetry(conn, event_name, clean_email, title, body, url, status_code, "FAILED", err_text, resolved_intern_id, dev_id)
                            logger.error(f"WebPushException for device {dev_id}: {ex}")

                    except Exception as ex:
                        _log_delivery_telemetry(conn, event_name, clean_email, title, body, url, 500, "FAILED", str(ex), resolved_intern_id, dev_id)
                        logger.error(f"General exception sending push to device {dev_id}: {ex}")

    threading.Thread(target=_worker, daemon=True).start()


# ──────────────────────────────────────────────────────────────────────────────
# Semantic Lifecycle Dispatch Helpers (Mapped directly to real events)
# ──────────────────────────────────────────────────────────────────────────────

def notify_application_status_push(email: str, name: str, status: str, notes: Optional[str] = None):
    """Fired when application review status changes."""
    status_map = {
        "Under Review": ("📄 Application Under Review", "Technical mentors are assessing your domain track and profile."),
        "Selected": ("🎉 You're Selected!", "Congratulations! You've been selected. Secure your seat on the portal."),
        "Enrollment Pending": ("💳 Complete Enrollment", "Please complete your balance enrollment to unlock milestones."),
        "Accepted": ("🏆 Welcome to DBERT!", "Your fellowship enrollment is confirmed. Sprints are ready."),
        "On Hold": ("⏳ Review On Hold", "Your review is temporarily on hold. Check notes for details."),
        "Rejected": ("Application Update", "Your application was not selected this time. You may re-apply in 30 days.")
    }
    title, body = status_map.get(status, ("📌 Application Update", f"Your status has updated to: {status}"))
    if notes:
        body += f" Note: {notes[:80]}"
    dispatch_lifecycle_push("application_status", target_email=email, title=title, body=body, url="/portal")


def notify_offer_signed_push(email: str, name: str, offer_id: str):
    """Fired when an intern digitally signs their offer letter."""
    dispatch_lifecycle_push(
        "offer_signed",
        target_email=email,
        title="✍️ Offer Letter Signed",
        body=f"Congratulations {name}! Your fellowship agreement ({offer_id}) is officially registered.",
        url="/portal"
    )


def notify_deposit_verified_push(email: str, name: str, amount: int = 499):
    """Fired when caution deposit is reconciled."""
    dispatch_lifecycle_push(
        "deposit_verified",
        target_email=email,
        title="💳 Caution Deposit Reconciled",
        body=f"Your ₹{amount} caution deposit credit has been confirmed and applied to your account.",
        url="/enroll/1999"
    )


def notify_balance_enrolled_push(email: str, name: str, domain: str):
    """Fired when the ₹1,500 balance is confirmed and seat is locked."""
    dispatch_lifecycle_push(
        "seat_confirmed",
        target_email=email,
        title="✅ Incubation Seat Confirmed",
        body=f"Your ₹1,500 balance is reconciled! You are officially enrolled in the {domain} sprint.",
        url="/portal"
    )


def notify_quiz_passed_push(email: str, course_id: int, day_number: int, course_title: str):
    """Fired when an intern passes a daily course quiz."""
    dispatch_lifecycle_push(
        "quiz_passed",
        target_email=email,
        title=f"🎯 Day {day_number} Passed!",
        body=f"Great work on {course_title}! Day {day_number + 1} has been unlocked.",
        url=f"/course/{course_id}"
    )


def notify_course_completed_push(email: str, course_title: str, cert_id: str):
    """Fired when a course is 100% completed and certificate is issued."""
    dispatch_lifecycle_push(
        "course_completed",
        target_email=email,
        title="🏆 Course Mastered!",
        body=f"Congratulations! You completed {course_title}. Your certificate ({cert_id}) is ready to verify.",
        url=f"/portal/certificate/{cert_id}"
    )


def notify_attendance_goal_push(email: str, hours_logged: float):
    """Fired when an intern achieves the weekly 10-hour portal attendance milestone."""
    dispatch_lifecycle_push(
        "attendance_goal",
        target_email=email,
        title="⏱️ Weekly Attendance Goal Met",
        body=f"Outstanding! You've logged {hours_logged:.1f} hours this week. Attendance requirement fulfilled.",
        url="/intern/attendance"
    )


def notify_attendance_streak_warning_push(email: str):
    """Fired when an intern has been inactive for 3 days to protect their sprint standing."""
    dispatch_lifecycle_push(
        "attendance_warning",
        target_email=email,
        title="⚠️ Keep Your Attendance Streak",
        body="You haven't logged portal hours in 3 days. Check in today to keep your standing active!",
        url="/portal"
    )


def notify_mentor_booking_push(email: str, mentor_name: str, slot_time: str, meet_link: str):
    """Fired when an intern reserves a seat in a 1-on-1 mentorship session."""
    dispatch_lifecycle_push(
        "mentor_booked",
        target_email=email,
        title="📅 Mentor Session Confirmed",
        body=f"1-on-1 with {mentor_name} reserved for {slot_time}. Meeting link ready.",
        url=meet_link or "/mentors/booking"
    )


def notify_bounty_published_push(task_id: int, title: str, reward_coins: int = 50, domain: str = ""):
    """Fired when a new bounty task is added to the catalog."""
    dispatch_lifecycle_push(
        "bounty_new",
        target_email=None,
        title=f"🪙 New {reward_coins}-Coin Bounty Available!",
        body=f"{title}. Submit your work to earn DBERT Coins.",
        url="/tasks",
        target_cohort=domain or "all"
    )


def notify_task_submitted_push(email: str, task_title: str):
    """Fired when an intern submits work on a task."""
    dispatch_lifecycle_push(
        "task_submitted",
        target_email=email,
        title="📝 Submission Received",
        body=f"Your submission for '{task_title}' was received and queued for staff review.",
        url="/tasks"
    )


def notify_task_approved_push(email: str, task_title: str, coins_awarded: int):
    """Fired when staff approves a submitted task and awards coins."""
    dispatch_lifecycle_push(
        "task_approved",
        target_email=email,
        title="🎉 Task Approved!",
        body=f"Your work for '{task_title}' was approved! +{coins_awarded} Coins credited to your wallet.",
        url="/intern/coins/ledger"
    )


def notify_task_revision_push(email: str, task_title: str, feedback: str = ""):
    """Fired when staff requests a revision on a submitted task."""
    body = f"Mentors requested revisions on '{task_title}'."
    if feedback:
        body += f" Feedback: {feedback[:80]}"
    dispatch_lifecycle_push(
        "task_revision",
        target_email=email,
        title="📝 Task Feedback & Revision Needed",
        body=body,
        url="/tasks"
    )


def notify_stipend_gate_cleared_push(email: str, gate_number: int, gate_name: str):
    """Fired when an intern satisfies a stipend gate requirement."""
    dispatch_lifecycle_push(
        "gate_cleared",
        target_email=email,
        title=f"🛡️ Gate {gate_number} Cleared!",
        body=f"You satisfied {gate_name}. 1 step closer to your 5,000 Coins stipend release.",
        url="/stipend/tasks"
    )


def notify_stipend_approved_push(email: str, coins: int = 5000):
    """Fired when the 5,000 Coins stipend contribution is officially approved."""
    dispatch_lifecycle_push(
        "stipend_approved",
        target_email=email,
        title="💰 Stipend Approved (+5,000 Coins)!",
        body=f"Congratulations! Your technical contribution was approved. {coins:,} Coins released for UPI withdrawal.",
        url="/intern/ambassador/withdraw"
    )


def notify_stipend_payout_dispatched_push(email: str, amount: int, utr: str):
    """Fired when admin completes the UPI transfer and inputs the UTR."""
    dispatch_lifecycle_push(
        "payout_dispatched",
        target_email=email,
        title="💸 Stipend Payout Sent via UPI!",
        body=f"₹{amount:,} has been transferred to your UPI ID (Bank UTR: {utr}).",
        url="/intern/coins/ledger"
    )


def notify_broadcast_push(title: str, body: str, url: str = "https://lms.dbert.in", target_cohort: str = "all"):
    """Fired from the Admin Push Broadcast Console."""
    dispatch_lifecycle_push(
        "broadcast",
        target_email=None,
        title=title,
        body=body,
        url=url,
        target_cohort=target_cohort
    )
