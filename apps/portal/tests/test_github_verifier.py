import sys
from pathlib import Path

PORTAL_DIR = Path(__file__).resolve().parent.parent
if str(PORTAL_DIR) not in sys.path:
    sys.path.insert(0, str(PORTAL_DIR))

from services.github_verifier import GitHubVerifier


def test_classify_official_pr():
    res = GitHubVerifier.classify_url("https://github.com/Alkameinc/alkame-nifty-50-educational/pull/7")
    assert res["status"] == "OFFICIAL_PR"
    assert res["is_official"] is True
    assert res["is_pr"] is True
    assert res["pr_number"] == 7


def test_classify_official_repo_without_pr():
    res = GitHubVerifier.classify_url("https://github.com/DBERT-INDIA/Internshipportal")
    assert res["status"] == "OFFICIAL_REPO_NO_PR"
    assert res["is_pr"] is False


def test_classify_fork_without_pr():
    res = GitHubVerifier.classify_url("https://github.com/someuser/alkame-nifty-50-educational")
    assert res["status"] == "FORK_NO_PR"
    assert res["is_official"] is False


def test_classify_unofficial_repo():
    res = GitHubVerifier.classify_url("https://github.com/someuser/my-todo-app")
    assert res["status"] == "UNOFFICIAL_REPO"
    assert res["is_official"] is False


def test_classify_profile_and_non_github():
    assert GitHubVerifier.classify_url("https://github.com/Sruthi247259")["status"] == "PROFILE_ONLY"
    assert GitHubVerifier.classify_url("https://princess-chinni.com")["status"] == "NON_GITHUB_URL"
    assert GitHubVerifier.classify_url("")["status"] == "MISSING"
