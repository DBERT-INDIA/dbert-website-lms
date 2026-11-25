"""
apps/portal/services/stipend_nudge_service.py
=============================================================================
DBERT Automated Stipend & Growth Nudge Engine
=============================================================================
Identifies eligible interns approaching or past their completion milestone
and dispatches high-converting step-by-step guidance emails to ensure 100%
completion of LinkedIn experience and engineering case studies.
"""

import json
import logging
import os
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from urllib.parse import quote

logger = logging.getLogger("stipend_nudge_service")


class StipendNudgeService:

    @staticmethod
    def _load_certificates_registry() -> Dict[str, Any]:
        """Loads local certificates registry to reconcile verified credentials."""
        candidates_map = {}
        # Potential registry locations
        paths = [
            os.path.join(os.path.dirname(__file__), "..", "..", "website", "src", "data", "certificates_registry.json"),
            "/var/www/dbert-website-lms/apps/website/src/data/certificates_registry.json",
            "src/data/certificates_registry.json"
        ]
        for p in paths:
            if os.path.exists(p):
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        for cert_id, c in data.items():
                            email = (c.get("holderEmail") or "").strip().lower()
                            if email:
                                candidates_map[email] = {
                                    "cert_id": cert_id,
                                    "is_verified": c.get("verified", False) and not c.get("isProvisional", False),
                                    "domain": c.get("domain", "")
                                }
                    break
                except Exception as ex:
                    logger.warning("Failed to load certificates registry from %s: %s", p, ex)
        return candidates_map

    @classmethod
    def get_funnel_stats(cls, conn) -> Dict[str, int]:
        """Calculates live KPI metrics for the stipend & growth funnel."""
        candidates = cls.get_eligible_candidates(conn, limit=1000)
        
        total = len(candidates)
        linkedin_count = sum(1 for c in candidates if c.get("g1_linkedin"))
        article_count = sum(1 for c in candidates if c.get("g2_article"))
        verified_count = sum(1 for c in candidates if c.get("g3_certified"))
        github_count = sum(1 for c in candidates if c.get("g4_github"))
        stipend_ready_count = sum(1 for c in candidates if c.get("unlocked_count") == 4)

        return {
            "total_candidates": total,
            "linkedin_verified": linkedin_count,
            "articles_published": article_count,
            "credentials_verified": verified_count,
            "github_linked": github_count,
            "stipend_ready": stipend_ready_count,
        }

    @classmethod
    def get_eligible_candidates(cls, conn, limit: int = 500) -> List[Dict[str, Any]]:
        """
        Extracts enrolled/accepted interns and evaluates their progression
        across the 4 core milestones (LinkedIn, Case Study, Credential, GitHub).
        """
        registry_map = cls._load_certificates_registry()

        # 1. Fetch all accepted enrolled candidates + accepted applications
        enrolled_query = """
            SELECT DISTINCT LOWER(TRIM(e.email)) AS email,
                   COALESCE(e.name, '') AS name,
                   COALESCE(e.domain, '') AS domain,
                   COALESCE(e.batch_label, '') AS batch_label,
                   COALESCE(e.phone, '') AS phone,
                   e.created_at AS enrolled_at
            FROM enrollments e
            WHERE e.payment_status = 'Accepted' 
              AND e.email IS NOT NULL AND TRIM(e.email) != ''
            
            UNION
            
            SELECT DISTINCT LOWER(TRIM(a.email)) AS email,
                   COALESCE(a.name, '') AS name,
                   COALESCE(a.domain, '') AS domain,
                   'Active Sprint' AS batch_label,
                   COALESCE(a.phone, '') AS phone,
                   a.created_at AS enrolled_at
            FROM applications a
            WHERE a.status = 'Accepted'
              AND a.email IS NOT NULL AND TRIM(a.email) != ''
            
            LIMIT ?
        """
        rows = conn.execute(enrolled_query, (limit,)).fetchall()
        
        candidates = []
        seen_emails = set()

        for r in rows:
            email = r["email"]
            if not email or email in seen_emails:
                continue
            seen_emails.add(email)

            name = r["name"] or "DBERT Fellow"
            domain = r["domain"] or "Engineering"
            batch_label = r["batch_label"] or "Active Cohort"

            # 2. Check intern_accounts for profile & links
            acct = conn.execute(
                """
                SELECT id, name, domain, college, linkedin_url, linkedin_verified, github_url, phone
                FROM intern_accounts
                WHERE LOWER(email) = ?
                LIMIT 1
                """,
                (email,)
            ).fetchone()

            intern_id = acct["id"] if acct else None
            phone = ""
            if acct and acct["phone"]:
                phone = str(acct["phone"]).strip()
            if not phone and "phone" in r.keys() and r["phone"]:
                phone = str(r["phone"]).strip()
            linkedin_url = (acct["linkedin_url"] or "").strip() if acct else ""
            github_url = (acct["github_url"] or "").strip() if acct else ""
            linkedin_verified = bool(acct and (acct["linkedin_verified"] or linkedin_url))

            # 3. Check published articles
            art_row = None
            if intern_id:
                art_row = conn.execute(
                    """
                    SELECT id, title, status, published_url
                    FROM intern_articles
                    WHERE intern_id = ?
                    ORDER BY id DESC LIMIT 1
                    """,
                    (intern_id,)
                ).fetchone()

            has_published_article = bool(art_row and (art_row["status"] or "").upper() == "PUBLISHED")
            has_article = bool(art_row)
            article_status = (art_row["status"] or "").upper() if art_row else "NOT_SUBMITTED"
            published_url = art_row["published_url"] if art_row else ""

            # 4. Check certificate verification status
            reg_entry = registry_map.get(email, {})
            cert_id = reg_entry.get("cert_id") or ""
            is_verified = reg_entry.get("is_verified", False)

            # Fallback to DB intern_certificates
            if not is_verified:
                cert_row = conn.execute(
                    """
                    SELECT cert_id, tier
                    FROM intern_certificates
                    WHERE LOWER(email) = ? OR intern_id = ?
                    LIMIT 1
                    """,
                    (email, intern_id or -1)
                ).fetchone()
                if cert_row:
                    cert_id = cert_row["cert_id"]
                    is_verified = True

            # Evaluate 4 gates
            g1 = bool(linkedin_verified)
            g2 = bool(has_published_article)
            g3 = bool(is_verified)
            g4 = bool(github_url)

            unlocked_count = sum([g1, g2, g3, g4])

            # Determine next in line action
            if not g1:
                next_step = "Link LinkedIn Profile"
                next_action = "LINK_LINKEDIN"
                action_url = "https://lms.dbert.in/profile"
            elif not g2:
                next_step = "Publish Case Study Article"
                next_action = "SUBMIT_ARTICLE"
                action_url = "https://lms.dbert.in/blog"
            elif not g3:
                next_step = "Verify Credential (₹299)"
                next_action = "VERIFY_CERTIFICATE"
                action_url = f"https://dbert.in/verify/unlock?email={email}" + (f"&certid={cert_id}" if cert_id else "")
            elif not g4:
                next_step = "Submit GitHub Repo & Demo"
                next_action = "SUBMIT_GITHUB"
                action_url = "https://lms.dbert.in/tasks"
            else:
                next_step = "₹5,000 Stipend Ready"
                next_action = "STIPEND_READY"
                action_url = "https://lms.dbert.in/stipend/tasks"

            # Clean phone for WhatsApp link
            clean_digits = re.sub(r"[^\d]", "", phone or "")
            if len(clean_digits) == 10:
                wa_phone = f"91{clean_digits}"
            elif len(clean_digits) == 12 and clean_digits.startswith("91"):
                wa_phone = clean_digits
            else:
                wa_phone = clean_digits

            # Pre-filled WhatsApp message
            wa_text = (
                f"Hi {name}, Admissions Team here from DBERT.\n\n"
                f"You are actively enrolled in the DBERT Technical Incubation Fellowship ({domain}). "
                f"To unlock your ₹5,000 Production Stipend release, your next required milestone is:\n\n"
                f"🎯 *{next_step}*\n"
                f"🔗 Complete here: {action_url}\n\n"
                f"Once submitted, our mentors will verify and clear this gate within 24 hours. "
                f"Reply here if you need any assistance."
            )
            wa_url = f"https://wa.me/{wa_phone}?text={quote(wa_text)}" if wa_phone else f"https://wa.me/?text={quote(wa_text)}"

            candidates.append({
                "intern_id": intern_id,
                "email": email,
                "name": name,
                "phone": phone,
                "domain": domain,
                "batch_label": batch_label,
                "cert_id": cert_id,
                "is_verified": is_verified,
                "linkedin_url": linkedin_url,
                "linkedin_verified": g1,
                "has_article": g2,
                "article_status": article_status,
                "published_url": published_url,
                "github_url": github_url,
                "g1_linkedin": g1,
                "g2_article": g2,
                "g3_certified": g3,
                "g4_github": g4,
                "unlocked_count": unlocked_count,
                "next_step": next_step,
                "next_action": next_action,
                "action_url": action_url,
                "wa_url": wa_url,
                "wa_text": wa_text,
            })

        # Sort: Highest unlocked gates and verified first
        candidates.sort(key=lambda x: (x["unlocked_count"], x["g3_certified"]), reverse=True)
        return candidates

    @staticmethod
    def send_eligibility_nudge(candidate: Dict[str, Any], send_fn) -> bool:
        """
        Dispatches Nudge email with clear, actionable step-by-step instructions.
        """
        email = candidate["email"]
        name = candidate["name"]
        domain = candidate["domain"]
        cert_id = candidate.get("cert_id", "")
        next_step = candidate.get("next_step", "Complete Milestones")

        subject = f"Action Required: Complete Your Next Step ({next_step}) to Unlock Your ₹5,000 DBERT Stipend"

        unlock_cta = ""
        if candidate.get("next_action") == "VERIFY_CERTIFICATE":
            unlock_link = f"https://dbert.in/verify/unlock?email={email}" + (f"&certid={cert_id}" if cert_id else "")
            unlock_cta = f'''
            <div style="text-align: center; margin: 10px 0 20px;">
              <a href="{unlock_link}" style="display: inline-block; background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%); color: #0F172A; text-decoration: none; font-weight: 800; padding: 12px 28px; border-radius: 8px; font-size: 14px; box-shadow: 0 4px 14px rgba(245,158,11,0.35);">
                Direct ₹299 Credential Verification Portal &rarr;
              </a>
            </div>
            '''

        html_body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #1e293b; line-height: 1.6; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; background: #ffffff;">
          <div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); padding: 28px; color: #ffffff; text-align: center;">
            <div style="display: inline-block; background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.4); color: #38BDF8; font-size: 11px; font-weight: 800; padding: 4px 12px; border-radius: 9999px; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 12px;">
              Stipend &amp; Growth Milestone
            </div>
            <h1 style="margin: 0; font-size: 20px; font-weight: 800; color: #ffffff;">Unlock Your ₹5,000 Production Stipend</h1>
            <p style="margin: 6px 0 0; font-size: 13px; color: #94A3B8;">DBERT Engineering &amp; Venture Incubation Fellowship</p>
          </div>

          <div style="padding: 24px 28px;">
            <p>Dear <strong>{name}</strong>,</p>
            <p>
              You are actively progressing toward your <strong>₹5,000 Technical Milestone Bounty</strong> in <strong>{domain}</strong>.
            </p>
            <div style="background: #F8FAFC; border-left: 4px solid #F59E0B; padding: 14px 16px; margin: 16px 0; border-radius: 0 8px 8px 0;">
              <strong style="color: #92400E; font-size: 14px;">Next Action Required:</strong>
              <p style="margin: 4px 0 0; font-size: 13.5px; color: #475569;">
                <strong>{next_step}</strong>. Please complete this milestone to unlock your stipend release.
              </p>
            </div>
            {unlock_cta}
            <div style="text-align: center; margin: 16px 0;">
              <a href="https://lms.dbert.in/#signin?email={email}" style="display: inline-block; background: #2563EB; color: #ffffff; text-decoration: none; font-weight: 700; padding: 12px 28px; border-radius: 8px; font-size: 14px;">
                Log into LMS Dashboard &rarr;
              </a>
            </div>
            <p style="font-size: 12.5px; color: #64748B;">
              Need support? Reach our Admissions concierge at <strong>+91 81929 11360</strong> or Academic Operations at <strong>+91 89580 06294</strong>.
            </p>
          </div>
        </div>
        """

        plain_body = f"Hello {name},\n\nPlease complete your next step: {next_step} to unlock your ₹5,000 stipend.\nLog into: https://lms.dbert.in/#signin?email={email}\n\nDBERT Operations"

        try:
            # send_email_async signature: (to_email, subject, html_body, name="", campaign="transactional")
            send_fn(to_email=email, subject=subject, html_body=html_body, name=name, campaign="stipend_nudge")
            return True
        except TypeError:
            try:
                send_fn(email, subject, html_body, name)
                return True
            except Exception as ex:
                logger.error("Failed to send eligibility nudge to %s: %s", email, ex)
                return False
        except Exception as ex:
            logger.error("Failed to send eligibility nudge to %s: %s", email, ex)
            return False
