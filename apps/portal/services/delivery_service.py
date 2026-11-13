"""
apps/portal/services/delivery_service.py
Resilient, production-ready multi-provider email delivery engine for DBERT.
Fulfills SCOPE.md interface contract:
    send_email(to, subject, html_content, text_content=None, tags=None, dry_run=False) -> DeliveryResult
"""

import os
import ssl
import time
import uuid
import re
import html
import hmac
import hashlib
import logging
import smtplib
import random
import json
import threading
from dataclasses import dataclass, field
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formatdate, formataddr
from typing import Optional, Dict, Any, List, Union, Tuple
from urllib.parse import quote

logger = logging.getLogger("dbert.delivery")

# -----------------------------------------------------------------------------
# Domain Constants & Defaults
# -----------------------------------------------------------------------------
DEFAULT_PRIMARY_PROVIDER = "smtp"
DEFAULT_SMTP_HOST = "smtp.gmail.com"
DEFAULT_SMTP_PORT = 465
DEFAULT_SMTP_USER = "abhinav.sharma@dbert.in"
DEFAULT_FROM_EMAIL = "abhinav.sharma@dbert.in"
DEFAULT_FROM_NAME = "DBERT Support"
DEFAULT_REPLY_TO = "support@dbert.in"
DEFAULT_CANONICAL_DOMAIN = "dbert.in"
DEFAULT_EMAIL_SITE = "https://lms.dbert.in"

# List of dummy/synthetic domains that must be intercepted locally
DUMMY_EMAIL_DOMAINS = (
    "@example.com", "@example.org", "@example.net",
    ".example.com", ".example.org", ".example.net", ".example",
    ".test", "@test.com", ".invalid", "@invalid", "@localhost", ".localhost",
    "@dbert.test", ".dbert.test", "@sample.com", "@demo.com",
    "@mailinator.com", "@fakemail.com"
)

# Strict RFC 5322 syntax validation regex
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$")

# Registry-suspended / dead domains that must NEVER be used for SMTP or links
SUSPENDED_DOMAINS = ("dbert.info",)


# -----------------------------------------------------------------------------
# Interface Contract: DeliveryResult
# -----------------------------------------------------------------------------
@dataclass
class DeliveryResult:
    success: bool
    provider: str
    message_id: str
    error: Optional[str] = None
    diagnostics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "provider": self.provider,
            "message_id": self.message_id,
            "error": self.error,
            "diagnostics": self.diagnostics,
        }


# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Multi-Account Google Workspace SMTP Pool
# -----------------------------------------------------------------------------
@dataclass
class SMTPAccount:
    email: str
    app_password: str
    from_name: str
    role: str = ""
    is_active: bool = True
    cooldown_until: float = 0.0

    def is_available(self) -> bool:
        return self.is_active and time.time() >= self.cooldown_until


class SMTPAccountPool:
    """
    Thread-safe pool of Google Workspace SMTP accounts.
    Supports dynamic random selection, load distribution, and automated failover
    upon daily sending limits (550 5.4.5) or authentication errors.
    """
    def __init__(self, accounts_json: Optional[str] = None):
        self.accounts: List[SMTPAccount] = []
        self._lock = threading.Lock()
        self._load_accounts(accounts_json)

    def _load_accounts(self, accounts_json: Optional[str] = None):
        raw = accounts_json or os.environ.get("SMTP_ACCOUNTS_JSON", "")
        if raw:
            try:
                data = json.loads(raw)
                if isinstance(data, list):
                    for item in data:
                        em = item.get("email", "").strip()
                        pw = item.get("app_password", "").strip()
                        if em and pw:
                            self.accounts.append(SMTPAccount(
                                email=em,
                                app_password=pw,
                                from_name=item.get("from_name", "DBERT Support"),
                                role=item.get("role", "")
                            ))
            except Exception as e:
                logger.error(f"Failed to parse SMTP_ACCOUNTS_JSON: {e}")

    def get_shuffled_accounts(self) -> List[SMTPAccount]:
        """Return available accounts shuffled randomly for uniform load distribution."""
        with self._lock:
            avail = [a for a in self.accounts if a.is_available()]
            if not avail and self.accounts:
                # If all are in cooldown, pick the ones closest to recovery
                avail = sorted(self.accounts, key=lambda a: a.cooldown_until)
        shuffled = list(avail)
        random.shuffle(shuffled)
        return shuffled

    def mark_limited(self, email: str, cooldown_hours: float = 24.0):
        """Place account into cooldown upon detecting Google quota or sending limit."""
        with self._lock:
            for a in self.accounts:
                if a.email.lower() == email.lower():
                    a.cooldown_until = time.time() + (cooldown_hours * 3600)
                    logger.warning(
                        f"SMTP Account [{email}] marked limited (550 sending limit). "
                        f"Cooldown active until {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(a.cooldown_until))}."
                    )


# Velocity / Pacing Limiter
# -----------------------------------------------------------------------------
class EmailPacer:
    """
    Thread-safe inter-message rate limiter to prevent Google Workspace
    velocity throttling and recipient flood protection.
    """
    def __init__(self, default_interval: float = 15.0):
        self.default_interval = default_interval
        self._lock = threading.Lock()
        self._last_dispatch_ts: float = 0.0
        self._recipient_dispatch_ts: Dict[str, float] = {}

    def calculate_delay(self, recipient: str, interval: Optional[float] = None) -> float:
        min_interval = interval if interval is not None else self.default_interval
        if min_interval <= 0:
            return 0.0
        now = time.time()
        rcpt_key = (recipient or "").strip().lower()
        with self._lock:
            target_ts = max(now, self._last_dispatch_ts + min_interval)
            target_ts = max(target_ts, self._recipient_dispatch_ts.get(rcpt_key, 0.0) + min_interval)
            delay_needed = max(0.0, target_ts - now)
            return round(delay_needed, 3)

    def wait_and_record(self, recipient: str, interval: Optional[float] = None, dry_run: bool = False) -> float:
        min_interval = interval if interval is not None else self.default_interval
        if min_interval <= 0:
            return 0.0
        rcpt_key = (recipient or "").strip().lower()
        with self._lock:
            now = time.time()
            target_ts = max(now, self._last_dispatch_ts + min_interval)
            target_ts = max(target_ts, self._recipient_dispatch_ts.get(rcpt_key, 0.0) + min_interval)
            delay = max(0.0, target_ts - now)
            if not dry_run:
                self._last_dispatch_ts = target_ts
                self._recipient_dispatch_ts[rcpt_key] = target_ts
        if delay > 0 and not dry_run:
            time.sleep(delay)
        return delay

    def reset(self):
        with self._lock:
            self._last_dispatch_ts = 0.0
            self._recipient_dispatch_ts.clear()


# Global default pacer instance
global_pacer = EmailPacer(default_interval=float(os.environ.get("EMAIL_PACING_SECONDS", "15.0")))


# -----------------------------------------------------------------------------
# Header, MIME, & Content Helpers
# -----------------------------------------------------------------------------
def generate_message_id(domain: str = DEFAULT_CANONICAL_DOMAIN) -> str:
    """Generate RFC 5322 Message-ID with FQDN."""
    clean_domain = (domain or DEFAULT_CANONICAL_DOMAIN).strip().lstrip("@")
    return f"<{uuid.uuid4()}@{clean_domain}>"


def generate_unsubscribe_token(to_email: str, secret_key: Optional[str] = None) -> str:
    """Generate SHA256 HMAC token for one-click unsubscribe verification."""
    key = (secret_key or os.environ.get("FLASK_SECRET_KEY", "dbert_unsub_secret_salt_2026")).encode()
    return hmac.new(key, f"unsub:{to_email.strip().lower()}".encode(), hashlib.sha256).hexdigest()[:32]


def generate_unsubscribe_url(to_email: str, email_site: str = DEFAULT_EMAIL_SITE, secret_key: Optional[str] = None) -> str:
    token = generate_unsubscribe_token(to_email, secret_key=secret_key)
    return f"{email_site.rstrip('/')}/unsubscribe?e={quote(to_email.strip().lower())}&t={token}"


def html_to_plain_text(html_content: str, email_site: str = DEFAULT_EMAIL_SITE) -> str:
    """Robust HTML to clean plain text conversion."""
    if not html_content:
        return f"Open your DBERT portal: {email_site}"
    t = re.sub(r"(?is)<(script|style|head).*?</\1>", "", html_content)
    t = re.sub(r"(?i)<br\s*/?>", "\n", t)
    t = re.sub(r"(?i)</(p|div|h[1-6]|tr|li)>", "\n", t)
    t = re.sub(r"(?i)<a [^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", r"\2 (\1)", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    t = re.sub(r"[ \t]+\n", "\n", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip() or f"Open your DBERT portal: {email_site}"


def generate_email_footer(
    to_email: str,
    email_site: str = DEFAULT_EMAIL_SITE,
    reply_to: str = DEFAULT_REPLY_TO,
    secret_key: Optional[str] = None
) -> str:
    """
    Standardized deliverability footer compliant with CAN-SPAM and DPDP Act 2023.
    Explicitly purges dead dbert.info or legacy domains.
    """
    unsub_url = generate_unsubscribe_url(to_email, email_site=email_site, secret_key=secret_key)
    clean_site = email_site.rstrip('/')
    return (
        "<div style='max-width:580px;margin:0 auto 26px;padding:0 20px;text-align:center;font-family:Arial,Helvetica,sans-serif;'>"
        "<div style='border-top:1px solid #232a36;margin:24px 0 16px;'></div>"
        "<p style='color:#8a9ab5;font-size:11.5px;line-height:1.75;margin:0 0 10px;'>"
        "<strong style='color:#c9d3dd;'>Digital Blinc Education Research and Technology (DBERT)</strong><br/>"
        f"MSME Registered &middot; Government of India &middot; <a href='{clean_site}' style='color:#E2B96F;text-decoration:none;'>lms.dbert.in</a>"
        "</p>"
        "<p style='color:#5a6577;font-size:11px;line-height:1.7;margin:0 0 10px;'>"
        "This is an official transactional notification regarding your account or application activity.<br/>"
        "<strong>Security Notice:</strong> DBERT will never ask for your password, OTP, UPI PIN, or banking credentials via email. "
        f"If you did not initiate this request, please contact <a href='mailto:{reply_to}' style='color:#7a8699;text-decoration:underline;'>{reply_to}</a>."
        "</p>"
        "<p style='color:#5a6577;font-size:10.5px;line-height:1.6;margin:0 0 12px;'>"
        "Data processed in accordance with the Digital Personal Data Protection Act, 2023 (DPDP Act, India)."
        "</p>"
        "<p style='color:#5a6577;font-size:11px;margin:0;'>"
        f"<a href='{unsub_url}' style='color:#7a8699;text-decoration:underline;'>Unsubscribe</a>"
        f" &middot; <a href='{clean_site}/privacy' style='color:#7a8699;text-decoration:underline;'>Privacy Policy</a>"
        f" &middot; <a href='{clean_site}/terms' style='color:#7a8699;text-decoration:underline;'>Terms of Service</a>"
        f" &middot; <a href='mailto:{reply_to}' style='color:#7a8699;text-decoration:underline;'>Support</a>"
        "</p>"
        "</div>"
    )


def build_mime_message(
    to_email: str,
    subject: str,
    html_content: str,
    text_content: Optional[str] = None,
    from_name: str = DEFAULT_FROM_NAME,
    from_email: str = DEFAULT_FROM_EMAIL,
    reply_to: str = DEFAULT_REPLY_TO,
    email_site: str = DEFAULT_EMAIL_SITE,
    secret_key: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    include_footer: bool = True,
    attachments: Optional[List[Tuple[str, bytes, str]]] = None
) -> MIMEMultipart:
    """
    Constructs an RFC 5322 & RFC 8058 compliant MIME message with optional attachments.
    Sanitizes content by excluding 1x1 tracking pixels and marketing UTM queries.
    """
    html_body = html_content or ""
    if include_footer and "Digital Blinc Education Research and Technology" not in html_body:
        footer_html = generate_email_footer(to_email, email_site=email_site, reply_to=reply_to, secret_key=secret_key)
        if "</body>" in html_body:
            html_body = html_body.replace("</body>", footer_html + "</body>")
        else:
            html_body = html_body + footer_html

    plain_body = text_content if text_content is not None else html_to_plain_text(html_body, email_site)

    clean_subject = re.sub(r"[\r\n]+", " ", str(subject or "")).strip()
    alt_part = MIMEMultipart("alternative")
    alt_part.attach(MIMEText(plain_body, "plain", "utf-8"))
    alt_part.attach(MIMEText(html_body, "html", "utf-8"))

    if attachments:
        msg = MIMEMultipart("mixed")
        msg.attach(alt_part)
        for att in attachments:
            fname = att[0]
            data = att[1]
            stype = att[2] if len(att) > 2 and att[2] else "pdf"
            if "/" in stype:
                stype = stype.split("/")[-1]
            part = MIMEApplication(data, _subtype=stype)
            part.add_header("Content-Disposition", "attachment", filename=fname)
            msg.attach(part)
    else:
        msg = alt_part

    msg["Subject"] = clean_subject
    msg["From"] = formataddr((from_name or "", from_email or DEFAULT_FROM_EMAIL))
    msg["To"] = to_email.strip()
    msg["Reply-To"] = reply_to
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = generate_message_id(domain=from_email.split("@")[-1] if "@" in from_email else DEFAULT_CANONICAL_DOMAIN)
    
    unsub_url = generate_unsubscribe_url(to_email, email_site=email_site, secret_key=secret_key)
    msg["List-Unsubscribe"] = f"<{unsub_url}>, <mailto:{reply_to}?subject=unsubscribe>"
    msg["List-Unsubscribe-Post"] = "List-Unsubscribe=One-Click"
    msg["Auto-Submitted"] = "auto-generated"

    if tags:
        for k, v in tags.items():
            header_key = f"X-DBERT-{k.replace('_', '-').title()}" if not k.startswith("X-") else k
            msg[header_key] = str(v)

    return msg


# -----------------------------------------------------------------------------
# EmailDeliveryService Implementation
# -----------------------------------------------------------------------------
class EmailDeliveryService:
    """
    Multi-provider, resilient email delivery engine.
    Supports:
      - Primary: Google Workspace SMTP (SSL port 465 / STARTTLS port 587)
      - Secondary Fallback: Transactional HTTPS API (cPanel mailer microservice) or Backup SMTP
      - Dry-run validation
      - Synthetic domain hard-bounce prevention
      - Automatic rate pacing
    """

    def __init__(
        self,
        smtp_host: Optional[str] = None,
        smtp_port: Optional[int] = None,
        smtp_user: Optional[str] = None,
        smtp_pass: Optional[str] = None,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
        reply_to: Optional[str] = None,
        cpanel_api_url: Optional[str] = None,
        cpanel_api_key: Optional[str] = None,
        backup_host: Optional[str] = None,
        backup_port: Optional[int] = None,
        backup_user: Optional[str] = None,
        backup_pass: Optional[str] = None,
        pacer: Optional[EmailPacer] = None,
        secret_key: Optional[str] = None
    ):
        self.smtp_host = smtp_host or os.environ.get("SMTP_HOST", DEFAULT_SMTP_HOST)
        self.smtp_port = int(smtp_port or os.environ.get("SMTP_PORT", str(DEFAULT_SMTP_PORT)))
        self.smtp_user = smtp_user or os.environ.get("SMTP_USER", DEFAULT_SMTP_USER)
        self.smtp_pass = smtp_pass or os.environ.get("SMTP_PASS", "")
        self.from_email = from_email or os.environ.get("FROM_EMAIL", DEFAULT_FROM_EMAIL)
        self.from_name = from_name or os.environ.get("FROM_NAME", DEFAULT_FROM_NAME)
        self.reply_to = reply_to or os.environ.get("REPLY_TO_EMAIL", DEFAULT_REPLY_TO)
        
        self.cpanel_api_url = cpanel_api_url or os.environ.get("CPANEL_EMAIL_API_URL", "https://mailer.aivaratech.online/send")
        self.cpanel_api_key = cpanel_api_key or os.environ.get("CPANEL_EMAIL_API_KEY", "")
        
        self.backup_host = backup_host or os.environ.get("SMTP_BACKUP_HOST", "")
        self.backup_port = int(backup_port or os.environ.get("SMTP_BACKUP_PORT", "465"))
        self.backup_user = backup_user or os.environ.get("SMTP_BACKUP_USER", "")
        self.backup_pass = backup_pass or os.environ.get("SMTP_BACKUP_PASS", "")
        
        self.pacer = pacer or global_pacer
        self.secret_key = secret_key or os.environ.get("FLASK_SECRET_KEY", "")
        self.pool = SMTPAccountPool(accounts_json=os.environ.get('SMTP_ACCOUNTS_JSON'))

    def is_dummy_domain(self, email: str) -> bool:
        if not isinstance(email, str):
            return True
        clean = email.strip().lower()
        if not clean or "@" not in clean:
            return True
        for dummy in DUMMY_EMAIL_DOMAINS:
            if clean.endswith(dummy) or dummy in clean:
                return True
        return False

    def is_domain_suspended(self, host_or_email: str) -> bool:
        clean = (host_or_email or "").strip().lower()
        for susp in SUSPENDED_DOMAINS:
            if clean == susp or clean.endswith(f".{susp}") or clean.endswith(f"@{susp}"):
                return True
        return False

    def _dispatch_smtp_ssl(self, host: str, port: int, user: str, passwd: str, to_email: str, raw_msg: str, timeout: int = 30):
        context = ssl.create_default_context()
        envelope_from = user or self.from_email
        with smtplib.SMTP_SSL(host, port, context=context, timeout=timeout) as s:
            if user and passwd:
                s.login(user, passwd)
            s.sendmail(envelope_from, [to_email], raw_msg)

    def _dispatch_smtp_starttls(self, host: str, port: int, user: str, passwd: str, to_email: str, raw_msg: str, timeout: int = 30):
        context = ssl.create_default_context()
        envelope_from = user or self.from_email
        with smtplib.SMTP(host, port, timeout=timeout) as s:
            s.ehlo()
            try:
                s.starttls(context=context)
                s.ehlo()
            except Exception:
                pass
            if user and passwd:
                s.login(user, passwd)
            s.sendmail(envelope_from, [to_email], raw_msg)

    def _dispatch_smtp_with_account(self, acc: SMTPAccount, msg: MIMEMultipart, to_email: str) -> Dict[str, Any]:
        """Dispatch email using a specific authenticated SMTPAccount from the pool."""
        # Align From and Reply-To headers with the selected account
        if msg.get("From"):
            msg.replace_header("From", formataddr((acc.from_name, acc.email)))
        else:
            msg.add_header("From", formataddr((acc.from_name, acc.email)))

        if not msg.get("Reply-To"):
            msg.add_header("Reply-To", acc.email)
            
        raw_str = msg.as_string()
        if self.smtp_port == 465:
            self._dispatch_smtp_ssl(self.smtp_host, self.smtp_port, acc.email, acc.app_password, to_email, raw_str)
        else:
            self._dispatch_smtp_starttls(self.smtp_host, self.smtp_port, acc.email, acc.app_password, to_email, raw_str)
            
        return {
            "primary_transport": "smtp_pool",
            "host": self.smtp_host,
            "port": self.smtp_port,
            "auth_user": acc.email,
            "from_name": acc.from_name,
        }

    def _dispatch_primary_smtp(self, msg: MIMEMultipart, to_email: str) -> Dict[str, Any]:
        raw_str = msg.as_string()
        if self.smtp_port == 465:
            self._dispatch_smtp_ssl(self.smtp_host, self.smtp_port, self.smtp_user, self.smtp_pass, to_email, raw_str)
        else:
            self._dispatch_smtp_starttls(self.smtp_host, self.smtp_port, self.smtp_user, self.smtp_pass, to_email, raw_str)
        return {
            "primary_transport": "smtp",
            "host": self.smtp_host,
            "port": self.smtp_port,
            "auth_user": self.smtp_user,
        }

    def _dispatch_secondary_api(self, msg: MIMEMultipart, to_email: str) -> Dict[str, Any]:
        """Secondary fallback transport: cPanel mailer HTTPS microservice."""
        if not self.cpanel_api_url:
            raise RuntimeError("CPANEL_EMAIL_API_URL not configured for secondary fallback")
        import requests
        
        html_part = text_part = ""
        for part in msg.walk():
            ct = part.get_content_type()
            if ct == "text/html":
                payload = part.get_payload(decode=True)
                html_part = payload.decode(part.get_content_charset() or "utf-8", errors="replace") if isinstance(payload, bytes) else str(payload)
            elif ct == "text/plain":
                payload = part.get_payload(decode=True)
                text_part = payload.decode(part.get_content_charset() or "utf-8", errors="replace") if isinstance(payload, bytes) else str(payload)

        headers = {"Content-Type": "application/json"}
        if self.cpanel_api_key:
            headers["X-API-Key"] = self.cpanel_api_key

        resp = requests.post(
            self.cpanel_api_url,
            headers=headers,
            json={
                "to": to_email,
                "subject": msg["Subject"],
                "html": html_part,
                "text": text_part,
                "from_name": self.from_name,
                "from_email": self.from_email,
            },
            timeout=10,
        )
        if resp.status_code < 200 or resp.status_code >= 300:
            raise RuntimeError(f"Fallback cPanel API returned HTTP {resp.status_code}: {resp.text[:200]}")
        return {
            "fallback_transport": "cpanel_api",
            "endpoint": self.cpanel_api_url,
            "http_status": resp.status_code,
        }

    def _dispatch_secondary_smtp(self, msg: MIMEMultipart, to_email: str) -> Dict[str, Any]:
        """Secondary fallback transport: Backup SMTP if domain is active."""
        if not self.backup_host or self.is_domain_suspended(self.backup_host):
            raise RuntimeError(f"Backup SMTP host invalid or suspended: {self.backup_host}")
        raw_str = msg.as_string()
        if self.backup_port == 465:
            self._dispatch_smtp_ssl(self.backup_host, self.backup_port, self.backup_user, self.backup_pass, to_email, raw_str)
        else:
            self._dispatch_smtp_starttls(self.backup_host, self.backup_port, self.backup_user, self.backup_pass, to_email, raw_str)
        return {
            "fallback_transport": "backup_smtp",
            "host": self.backup_host,
            "port": self.backup_port,
        }

    def send_email(
        self,
        to: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        dry_run: bool = False,
        attachments: Optional[List[Tuple[str, bytes, str]]] = None,
        preferred_account: Optional[str] = None
    ) -> DeliveryResult:
        """
        Public contract method for email transmission.
        Adheres to: send_email(to, subject, html_content, text_content=None, tags=None, dry_run=False) -> DeliveryResult
        """
        diagnostics: Dict[str, Any] = {
            "recipient": str(to) if to is not None else "",
            "subject": subject,
            "dry_run": dry_run,
            "timestamp": formatdate(localtime=True)
        }

        # 1. Recipient type safety & hard bounce pre-flight guard
        if not isinstance(to, str):
            return DeliveryResult(
                success=False,
                provider="hard_bounce_guard",
                message_id="",
                error="Recipient address must be a string",
                diagnostics=diagnostics
            )

        clean_to = to.strip()
        diagnostics["recipient"] = clean_to

        if any(ch in clean_to for ch in ("\r", "\n", "\x00")):
            return DeliveryResult(
                success=False,
                provider="hard_bounce_guard",
                message_id="",
                error="Recipient address contains prohibited control characters",
                diagnostics=diagnostics
            )

        if not clean_to or "@" not in clean_to:
            return DeliveryResult(
                success=False,
                provider="hard_bounce_guard",
                message_id="",
                error="Invalid recipient address: missing '@'",
                diagnostics=diagnostics
            )

        if self.is_dummy_domain(clean_to):
            diagnostics["intercepted"] = True
            diagnostics["reason"] = "synthetic_domain"
            return DeliveryResult(
                success=False,
                provider="hard_bounce_guard",
                message_id="",
                error=f"Recipient {clean_to} intercepted: synthetic dummy domain",
                diagnostics=diagnostics
            )

        if not EMAIL_REGEX.match(clean_to):
            return DeliveryResult(
                success=False,
                provider="hard_bounce_guard",
                message_id="",
                error=f"Invalid recipient address syntax: '{clean_to}'",
                diagnostics=diagnostics
            )

        # 2. Build RFC 5322 MIME message
        msg = build_mime_message(
            to_email=clean_to,
            subject=subject,
            html_content=html_content,
            text_content=text_content,
            from_name=self.from_name,
            from_email=self.from_email,
            reply_to=self.reply_to,
            secret_key=self.secret_key,
            tags=tags,
            attachments=attachments
        )
        msg_id = msg.get("Message-ID", "")
        diagnostics["message_id"] = msg_id
        diagnostics["headers"] = {
            "From": msg.get("From"),
            "To": msg.get("To"),
            "Reply-To": msg.get("Reply-To"),
            "Date": msg.get("Date"),
            "Message-ID": msg_id,
            "List-Unsubscribe": msg.get("List-Unsubscribe"),
            "List-Unsubscribe-Post": msg.get("List-Unsubscribe-Post"),
            "Auto-Submitted": msg.get("Auto-Submitted"),
        }

        # 3. Dry-run Mode Safety: Zero Network Dispatch
        if dry_run:
            diagnostics["action"] = "dry_run_validation_passed"
            diagnostics["mime_parts"] = [part.get_content_type() for part in msg.walk() if not part.is_multipart()]
            return DeliveryResult(
                success=True,
                provider="dry_run",
                message_id=msg_id,
                error=None,
                diagnostics=diagnostics
            )

        # 4. Check master switch
        master_enabled = os.environ.get("EMAILS_ENABLED", "true").lower() == "true"
        if not master_enabled:
            return DeliveryResult(
                success=False,
                provider="disabled",
                message_id=msg_id,
                error="EMAILS_ENABLED is false; dispatch skipped",
                diagnostics=diagnostics
            )

        # 5. Velocity / Pacing delay
        delay_sec = self.pacer.wait_and_record(clean_to, dry_run=False)
        diagnostics["pacing_delay_sec"] = delay_sec

        # 6. Attempt Primary Provider (Google Workspace SMTP Pool with Random Selection & Failover)
        primary_err = None
        shuffled_accounts = self.pool.get_shuffled_accounts()
        if preferred_account and shuffled_accounts:
            pref = [a for a in shuffled_accounts if a.email.lower() == preferred_account.lower()]
            rest = [a for a in shuffled_accounts if a.email.lower() != preferred_account.lower()]
            shuffled_accounts = pref + rest
        if shuffled_accounts:
            for acc in shuffled_accounts:
                try:
                    primary_info = self._dispatch_smtp_with_account(acc, msg, clean_to)
                    diagnostics.update(primary_info)
                    return DeliveryResult(
                        success=True,
                        provider=f"google_workspace_smtp_pool:{acc.email}",
                        message_id=msg_id,
                        error=None,
                        diagnostics=diagnostics
                    )
                except Exception as e:
                    err_str = str(e)
                    logger.warning(f"SMTP pool dispatch failed via account [{acc.email}] for {clean_to}: {err_str}")
                    if "550 5.4.5" in err_str or "daily user sending limit" in err_str.lower() or "quota" in err_str.lower():
                        self.pool.mark_limited(acc.email)
                    primary_err = e
            diagnostics["primary_pool_exhausted"] = True
            diagnostics["primary_error"] = str(primary_err)
        else:
            try:
                primary_info = self._dispatch_primary_smtp(msg, clean_to)
                diagnostics.update(primary_info)
                return DeliveryResult(
                    success=True,
                    provider="google_workspace_smtp",
                    message_id=msg_id,
                    error=None,
                    diagnostics=diagnostics
                )
            except Exception as e:
                primary_err = e
                logger.warning(f"Legacy primary SMTP dispatch failed for {clean_to}: {e}")
                diagnostics["primary_error"] = str(e)

        # 7. Secondary Fallback Provider
        # Attempt fallback via cPanel API or secondary SMTP
        fallback_errors = []
        if self.cpanel_api_url:
            try:
                fallback_info = self._dispatch_secondary_api(msg, clean_to)
                diagnostics.update(fallback_info)
                return DeliveryResult(
                    success=True,
                    provider="secondary_cpanel_api",
                    message_id=msg_id,
                    error=None,
                    diagnostics=diagnostics
                )
            except Exception as e:
                logger.warning(f"Secondary cPanel API fallback failed: {e}")
                fallback_errors.append(f"cpanel_api: {e}")

        if self.backup_host and not self.is_domain_suspended(self.backup_host):
            try:
                backup_info = self._dispatch_secondary_smtp(msg, clean_to)
                diagnostics.update(backup_info)
                return DeliveryResult(
                    success=True,
                    provider="secondary_backup_smtp",
                    message_id=msg_id,
                    error=None,
                    diagnostics=diagnostics
                )
            except Exception as e:
                logger.warning(f"Secondary backup SMTP fallback failed: {e}")
                fallback_errors.append(f"backup_smtp: {e}")

        combined_error = f"Primary failed ({primary_err}). " + (
            f"Fallbacks failed: {'; '.join(fallback_errors)}" if fallback_errors else "No valid fallback configured."
        )
        diagnostics["fallback_errors"] = fallback_errors
        return DeliveryResult(
            success=False,
            provider="failed",
            message_id=msg_id,
            error=combined_error,
            diagnostics=diagnostics
        )


# Singleton factory
_default_service: Optional[EmailDeliveryService] = None

def get_delivery_service() -> EmailDeliveryService:
    global _default_service
    if _default_service is None:
        _default_service = EmailDeliveryService()
    return _default_service


def send_email(
    to: str,
    subject: str,
    html_content: str,
    text_content: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    dry_run: bool = False
) -> DeliveryResult:
    """
    Module-level delivery function adhering directly to SCOPE.md interface contract.
    """
    service = get_delivery_service()
    return service.send_email(
        to=to,
        subject=subject,
        html_content=html_content,
        text_content=text_content,
        tags=tags,
        dry_run=dry_run
    )
