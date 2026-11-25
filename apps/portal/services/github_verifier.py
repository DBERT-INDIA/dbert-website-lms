import re
from typing import Any, Dict, Optional
import requests

OFFICIAL_ORGS = {
    "alkameinc",
    "ainabhinavsharma",
    "gayatri-education",
    "dbert-india",
    "aivara-technologies",
    "aivaratechinfomatics",
}

OFFICIAL_REPOS = {
    "alkame-nifty-50-educational",
    "gayatri-demo",
    "gayatri-ai",
    "gayatri-tutor-v3",
    "gayatribot-hr",
    "dbert-agent",
    "aivara-insight-lite",
    "internshipportal",
}


class GitHubVerifier:
    """Validates intern GitHub URLs and Pull Requests against DBERT's 4 official product ecosystems."""

    @staticmethod
    def classify_url(url: Optional[str]) -> Dict[str, Any]:
        if not url or not isinstance(url, str) or not url.strip():
            return {
                "status": "MISSING",
                "is_official": False,
                "is_pr": False,
                "org": "",
                "repo": "",
                "pr_number": None,
                "username": "",
                "message": "No GitHub URL provided.",
            }

        clean = url.strip().rstrip("/").replace(".git", "")
        if "github.com" not in clean.lower():
            return {
                "status": "NON_GITHUB_URL",
                "is_official": False,
                "is_pr": False,
                "org": "",
                "repo": "",
                "pr_number": None,
                "username": "",
                "message": "Submitted URL is not a github.com link.",
            }

        pr_match = re.search(r"github\.com/([^/]+)/([^/]+)/pull/(\d+)", clean, re.IGNORECASE)
        if pr_match:
            org = pr_match.group(1)
            repo = pr_match.group(2)
            pr_num = int(pr_match.group(3))
            is_official = (org.lower() in OFFICIAL_ORGS) or any(r in repo.lower() for r in OFFICIAL_REPOS)
            return {
                "status": "OFFICIAL_PR" if is_official else "UNOFFICIAL_PR",
                "is_official": is_official,
                "is_pr": True,
                "org": org,
                "repo": repo,
                "pr_number": pr_num,
                "username": "",
                "message": (
                    f"Pull Request #{pr_num} on {org}/{repo}."
                    if is_official
                    else f"Pull Request #{pr_num} is on an external repository ({org}/{repo}), not one of DBERT's 4 official product repos."
                ),
            }

        repo_match = re.search(r"github\.com/([^/]+)/([^/?#]+)", clean, re.IGNORECASE)
        if repo_match:
            org = repo_match.group(1)
            repo = repo_match.group(2)
            in_official_org = org.lower() in OFFICIAL_ORGS
            matches_official_repo = any(r in repo.lower() for r in OFFICIAL_REPOS)
            if in_official_org:
                status = "OFFICIAL_REPO_NO_PR"
                msg = f"Base official repository ({org}/{repo}) submitted without a direct Pull Request (/pull/<id>) link."
            elif matches_official_repo:
                status = "FORK_NO_PR"
                msg = f"Personal fork ({org}/{repo}) submitted without an upstream Pull Request link to the official DBERT/Alkame/Gayatri/Aivara repo."
            else:
                status = "UNOFFICIAL_REPO"
                msg = f"Standalone repository ({org}/{repo}) is not one of the 4 official DBERT product repositories."
            return {
                "status": status,
                "is_official": False,
                "is_pr": False,
                "org": org,
                "repo": repo,
                "pr_number": None,
                "username": org,
                "message": msg,
            }

        prof_match = re.search(r"github\.com/([^/?#]+)$", clean, re.IGNORECASE)
        if prof_match:
            user = prof_match.group(1)
            return {
                "status": "PROFILE_ONLY",
                "is_official": False,
                "is_pr": False,
                "org": "",
                "repo": "",
                "pr_number": None,
                "username": user,
                "message": f"GitHub profile ({user}) submitted instead of a Pull Request URL.",
            }

        return {
            "status": "INVALID_FORMAT",
            "is_official": False,
            "is_pr": False,
            "org": "",
            "repo": "",
            "pr_number": None,
            "username": "",
            "message": "Unrecognized GitHub URL format.",
        }

    @staticmethod
    def verify_pr_via_api(org: str, repo: str, pr_number: int, timeout: int = 6) -> Dict[str, Any]:
        """Queries GitHub REST API to verify PR existence, merge status, and author."""
        api_url = f"https://api.github.com/repos/{org}/{repo}/pulls/{pr_number}"
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "DBERT-Portal-Verifier/1.0",
        }
        try:
            resp = requests.get(api_url, headers=headers, timeout=timeout)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "api_checked": True,
                    "exists": True,
                    "state": data.get("state", ""),
                    "merged": bool(data.get("merged")),
                    "author": (data.get("user") or {}).get("login", ""),
                    "title": data.get("title", ""),
                    "html_url": data.get("html_url", ""),
                }
            return {
                "api_checked": True,
                "exists": False,
                "status_code": resp.status_code,
                "state": "not_found",
                "merged": False,
                "author": "",
            }
        except Exception as exc:
            return {
                "api_checked": False,
                "exists": None,
                "error": str(exc),
                "merged": False,
                "author": "",
            }
