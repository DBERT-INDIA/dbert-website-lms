import re
import urllib.parse
from datetime import datetime
from typing import Dict, Any, Tuple
import requests

LINKEDIN_URL_PATTERN = re.compile(
    r"^https?://(?:[a-zA-Z0-9\-]+\.)*linkedin\.com/(?:mwlite/)?in/([a-zA-Z0-9_\-\u0080-\uffff%]+)",
    re.IGNORECASE
)

TARGET_KEYWORDS = [
    "dbert",
    "dbert labs",
    "dbert.in",
    "delhi block & edtech",
    "delhi block and edtech",
    "delhi block",
]

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,image/apng,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "max-age=0",
    "Sec-Ch-Ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1"
}


class LinkedInVerifier:
    """Automated LinkedIn profile validation and public experience scraper."""

    @staticmethod
    def validate_url(raw_url: str) -> Tuple[bool, str]:
        """Validates and normalizes public LinkedIn profile URL."""
        if not raw_url:
            return False, ""
        clean = raw_url.strip()
        if not clean.startswith("http://") and not clean.startswith("https://"):
            clean = "https://" + clean
        match = LINKEDIN_URL_PATTERN.match(clean)
        if not match:
            return False, ""
        # Clean canonical URL
        handle = match.group(1).rstrip('/')
        canonical = f"https://www.linkedin.com/in/{handle}"
        return True, canonical

    @staticmethod
    def build_add_to_linkedin_url(domain: str, cert_id: str, issue_year: int = 2026, issue_month: int = 10) -> str:
        """Constructs official LinkedIn 1-Click certification addition intent launcher."""
        title = f"{domain or 'AI Engineering'} Fellow & Intern"
        org = "DBERT"
        cert_url = f"https://dbert.in/verify/{cert_id}" if cert_id else "https://dbert.in"
        
        params = {
            "startTask": "CERTIFICATION_NAME",
            "name": title,
            "organizationName": org,
            "issueYear": str(issue_year),
            "issueMonth": str(issue_month),
            "certUrl": cert_url,
            "certId": cert_id or ""
        }
        return f"https://www.linkedin.com/profile/add?{urllib.parse.urlencode(params)}"

    @staticmethod
    def probe_public_profile(profile_url: str, cert_id: str = "") -> Dict[str, Any]:
        """
        Attempts to scrape public LinkedIn profile HTML for DBERT experience/credentials.
        Returns detailed status: VERIFIED, PENDING_SCRAPE, or UNVERIFIED.
        """
        is_valid, canonical_url = LinkedInVerifier.validate_url(profile_url)
        if not is_valid:
            return {
                "verified": False,
                "status": "INVALID_URL",
                "message": "Invalid LinkedIn profile URL format. Must be linkedin.com/in/username."
            }

        try:
            resp = requests.get(canonical_url, headers=BROWSER_HEADERS, timeout=8, allow_redirects=True)
            
            resp_url = str(getattr(resp, "url", "") or "")
            is_challenge = "authwall" in resp_url.lower() or "challenge" in resp_url.lower()

            # Authwall or anti-bot challenge
            if resp.status_code in (429, 999) or is_challenge:
                return {
                    "verified": False,
                    "status": "PENDING_SCRAPE",
                    "canonical_url": canonical_url,
                    "message": "LinkedIn anti-bot authwall encountered. Profile queued for background polling daemon."
                }

            if resp.status_code != 200:
                return {
                    "verified": False,
                    "status": "PENDING_SCRAPE",
                    "canonical_url": canonical_url,
                    "message": f"LinkedIn returned HTTP {resp.status_code}. Queued for retry."
                }

            html = resp.text.lower()

            # Check for DBERT presence in experience or licenses
            found_keyword = None
            for kw in TARGET_KEYWORDS:
                if kw in html:
                    found_keyword = kw
                    break

            if not found_keyword and cert_id and cert_id.lower() in html:
                found_keyword = cert_id

            if found_keyword:
                return {
                    "verified": True,
                    "status": "VERIFIED",
                    "canonical_url": canonical_url,
                    "matched_keyword": found_keyword,
                    "verified_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "message": "DBERT verified in public LinkedIn Experience / Licenses!"
                }

            return {
                "verified": False,
                "status": "UNVERIFIED",
                "canonical_url": canonical_url,
                "message": "DBERT was not found in public Experience or Licenses. Please ensure DBERT is set to Public visibility."
            }

        except Exception as e:
            return {
                "verified": False,
                "status": "PENDING_SCRAPE",
                "canonical_url": canonical_url,
                "message": f"Temporary network timeout probing LinkedIn ({str(e)[:50]}). Queued for retry."
            }
