"""Run local smoke checks with the tools and dependencies already installed."""

import argparse
import ast
from pathlib import Path
import shutil
import subprocess
import sys

import yaml
from jinja2 import Environment


ROOT = Path(__file__).resolve().parents[1]
PORTAL = ROOT / "apps" / "portal"
WEBSITE = ROOT / "apps" / "website"
API_PACKAGE = ROOT / "dbert-api-package"


def _verify_compose_services():
    base = yaml.safe_load((API_PACKAGE / "docker-compose.yml").read_text(encoding="utf-8"))["services"]
    override = yaml.safe_load((API_PACKAGE / "docker-compose.override.yml").read_text(encoding="utf-8"))["services"]
    effective = {
        name: {**base.get(name, {}), **override.get(name, {})}
        for name in base.keys() | override.keys()
    }
    for name, service in effective.items():
        if not (service.get("image") or service.get("build")):
            raise ValueError(f"Compose service {name} needs an image or build.")
        for dependency in service.get("depends_on", ()):
            if dependency not in effective:
                raise ValueError(f"Compose service {name} depends on missing service {dependency}.")
    database = effective["db"]
    if not database.get("image", "").startswith("postgres:") or "db" not in effective["backend"]["depends_on"]:
        raise ValueError("Backend must depend on the PostgreSQL db service.")
    if "127.0.0.1:5432:5432" not in database.get("ports", ()):
        raise ValueError("Development database port must be published to localhost.")
    print("PASS Compose service and dependency checks", flush=True)


def _verify_portal_syntax():
    ast.parse((PORTAL / "app.py").read_text(encoding="utf-8-sig"), filename="apps/portal/app.py")
    environment = Environment()
    for template in sorted((PORTAL / "templates").glob("*.html")):
        environment.parse(template.read_text(encoding="utf-8-sig"), name=template.name)
    print("PASS Flask and portal Jinja syntax", flush=True)


def _run(label, argv, directory):
    print(f"Running {label}", flush=True)
    subprocess.run(argv, cwd=directory, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", action="store_true", help="include the preinstalled Chromium smoke suite")
    options = parser.parse_args()
    node = shutil.which("node")
    if not node:
        parser.error("Node.js 22 or newer is required for the website smoke checks.")
    try:
        _verify_compose_services()
        _verify_portal_syntax()
        pytest = [sys.executable, "-B", "-m", "pytest", "--noconftest", "-p", "no:cacheprovider", "-q"]
        _run("Flask workflows and SQLite transaction tests", [
            *pytest, "tests/test_enrollment_payment_claims.py", "tests/test_gateway_capture.py",
            "tests/test_task_review_queue.py", "tests/test_mentor_schedule.py", "tests/test_hiring_workflows.py",
            "tests/learning/test_turn_transaction_offline.py", "tests/unit/test_product_tools_offline.py",
            "tests/unit/test_quiz_recovery_offline.py", "tests/unit/test_job_fit_offline.py",
            "tests/unit/test_delivery_and_publication_offline.py", "tests/unit/test_project_workspace_offline.py",
            "tests/unit/test_course_publishing_offline.py", "tests/unit/test_verified_portfolio_offline.py",
            "tests/unit/test_program_cohorts_offline.py", "tests/unit/test_cohort_progress_offline.py",
            "tests/unit/test_study_classroom_offline.py", "tests/unit/test_cohort_certificate_integration_offline.py",
            "tests/test_application_state_machine.py", "tests/test_enrollment_state_machine.py",
            "tests/test_database_abstraction.py", "tests/test_postgres_enforcement.py",
            "tests/test_delivery_service.py", "tests/learning/test_adaptive_backtest.py",
            "tests/unit/test_scalability_configs.py", "tests/unit/test_gemini_discovery.py",
            "--deselect=tests/test_delivery_service.py::test_rfc8058_unsubscribe_route_get_and_post",
        ], PORTAL)
        _run("website payment intake tests", [
            node, "--experimental-strip-types", "--test", "scripts/test-enrollment-payment-claim.mjs",
            "scripts/test-website-payment-contract.mjs",
        ], WEBSITE)
        _run("website SEO metadata", [node, "scripts/check-seo.mjs"], WEBSITE)
        if options.browser:
            _run("résumé checker, course quiz, and study classroom browser tests", [
                *pytest, "tests/e2e/test_resume_checker.py", "tests/e2e/test_course_quiz_offline.py",
                "tests/e2e/test_study_classroom.py",
            ], PORTAL)
    except (OSError, ValueError, KeyError, SyntaxError, subprocess.CalledProcessError) as error:
        print(f"FAIL {error}", file=sys.stderr)
        return 1
    print("Offline smoke checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
