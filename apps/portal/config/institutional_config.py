"""
config/institutional_config.py - Centralized Institutional Leadership & Contact Coordinates

Single source of truth for all leadership signatories, admissions/support contact numbers,
official emails, physical office addresses, and domain origins across the DBERT portal.
Each value supports runtime override via environment variables.
"""

import os
from typing import Dict, Any

# Institutional Leadership & Signatories
DIRECTOR_NAME: str = os.environ.get("DBERT_DIRECTOR_NAME", "Mr. Abhinav Sharma").strip()
DIRECTOR_TITLE: str = os.environ.get("DBERT_DIRECTOR_TITLE", "Director & Research Lead").strip()
ORGANIZATION_NAME: str = os.environ.get("DBERT_ORGANIZATION_NAME", "Deep Bio Engineering Research & Training").strip()
ORGANIZATION_SHORT_NAME: str = "DBERT"

# Support & Admissions Coordinates
ADMISSIONS_PHONE: str = os.environ.get("DBERT_ADMISSIONS_PHONE", "+91 81929 11360").strip()
ADMISSIONS_WHATSAPP: str = os.environ.get("DBERT_ADMISSIONS_WHATSAPP", "918192911360").strip()
SUPPORT_PHONE: str = os.environ.get("DBERT_SUPPORT_PHONE", "+91 89580 06294").strip()
ADMISSIONS_EMAIL: str = os.environ.get("DBERT_ADMISSIONS_EMAIL", "admissions@dbert.in").strip()
SUPPORT_EMAIL: str = os.environ.get("DBERT_SUPPORT_EMAIL", "support@dbert.in").strip()
OFFICIAL_REPLY_TO: str = os.environ.get("DBERT_REPLY_TO_EMAIL", "abhinav.sharma@dbert.in").strip()

# Sovereign Domain Origins (Mandate: dbert.in only, never dbert.online)
SOVEREIGN_DOMAIN: str = "https://dbert.in"
LMS_DOMAIN: str = "https://lms.dbert.in"
API_DOMAIN: str = "https://api.dbert.in"

# Office & Institutional Physical Coordinates
HEADQUARTERS_ADDRESS: str = os.environ.get(
    "DBERT_HQ_ADDRESS",
    "Cyber Park, Sector 62, Gurugram, Haryana 122002, India"
).strip()
REGIONAL_OFFICE_ADDRESS: str = os.environ.get(
    "DBERT_REGIONAL_ADDRESS",
    "Janakpuri District Centre, New Delhi 110058, India"
).strip()


def get_institutional_context() -> Dict[str, Any]:
    """Returns a dict suitable for injection into template context processors or APIs."""
    return {
        "director_name": DIRECTOR_NAME,
        "director_title": DIRECTOR_TITLE,
        "organization_name": ORGANIZATION_NAME,
        "organization_short": ORGANIZATION_SHORT_NAME,
        "admissions_phone": ADMISSIONS_PHONE,
        "admissions_whatsapp": ADMISSIONS_WHATSAPP,
        "support_phone": SUPPORT_PHONE,
        "admissions_email": ADMISSIONS_EMAIL,
        "support_email": SUPPORT_EMAIL,
        "reply_to": OFFICIAL_REPLY_TO,
        "sovereign_domain": SOVEREIGN_DOMAIN,
        "lms_domain": LMS_DOMAIN,
        "api_domain": API_DOMAIN,
        "hq_address": HEADQUARTERS_ADDRESS,
        "regional_address": REGIONAL_OFFICE_ADDRESS,
    }
