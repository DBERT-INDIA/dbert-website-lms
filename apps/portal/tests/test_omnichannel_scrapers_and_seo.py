import pytest
import json
import sys
import os

# Add root and portal to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.scrapers.base import (
    CANONICAL_DOMAINS,
    normalize_domain,
    slugify,
    generate_fingerprint,
    ScrapedItem
)
from app import app, get_db

def test_canonical_domains_count():
    assert len(CANONICAL_DOMAINS) == 9
    expected = [
        "AI Agent Development",
        "Cybersecurity",
        "Data Analyst",
        "DevOps & Cloud",
        "Digital Marketing",
        "Full Stack Development",
        "Mobile App Development",
        "Python Automation",
        "UI/UX Design"
    ]
    assert sorted(CANONICAL_DOMAINS) == sorted(expected)

def test_normalize_domain_all_nine():
    samples = {
        "AI Agent Engineer (LLM & LangChain)": "AI Agent Development",
        "Junior SOC Analyst & Ethical Hacker": "Cybersecurity",
        "Data Analyst (SQL, Tableau & Power BI)": "Data Analyst",
        "DevOps & Kubernetes Cloud Intern": "DevOps & Cloud",
        "Performance Marketing & SEO Specialist": "Digital Marketing",
        "Full Stack React / Node Developer": "Full Stack Development",
        "Android / Flutter Mobile Developer": "Mobile App Development",
        "Python Automation & RPA Scripting": "Python Automation",
        "UI/UX Product Designer (Figma)": "UI/UX Design"
    }
    for title, expected_domain in samples.items():
        assert normalize_domain(title) == expected_domain, f"Failed for {title}"

def test_fingerprint_idempotency():
    fp1 = generate_fingerprint("Swiggy", "Analytics Intern", "Data Analyst", "Hybrid")
    fp2 = generate_fingerprint("swiggy", "analytics intern", "data analyst", "hybrid")
    fp3 = generate_fingerprint("Swiggy ", " Analytics Intern", "Data Analyst", "hybrid ")
    assert fp1 == fp2 == fp3

    fp_diff = generate_fingerprint("Swiggy", "Frontend Intern", "Full Stack Development", "Hybrid")
    assert fp1 != fp_diff

@pytest.fixture
def seed_test_company():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scraped_internships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Domain TEXT,
                Company TEXT,
                Role TEXT,
                Location TEXT,
                Is_Remote TEXT,
                Start_Date TEXT,
                End_Date TEXT,
                Stipend TEXT,
                URL TEXT,
                Description TEXT,
                Source TEXT,
                Region TEXT,
                Stipend_Normalized TEXT,
                Work_Model TEXT,
                City TEXT,
                Clicks INTEGER DEFAULT 0
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scraped_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Domain TEXT,
                Company TEXT,
                Role TEXT,
                Location TEXT,
                Is_Remote TEXT,
                Start_Date TEXT,
                End_Date TEXT,
                Stipend TEXT,
                URL TEXT,
                Description TEXT,
                Source TEXT,
                Region TEXT,
                Stipend_Normalized TEXT,
                Work_Model TEXT,
                City TEXT,
                Clicks INTEGER DEFAULT 0
            )
        """)
        conn.execute("""
            INSERT OR REPLACE INTO scraped_internships (
                id, Domain, Company, Role, Location, Is_Remote, Start_Date, End_Date,
                Stipend, URL, Description, Source, Region, Stipend_Normalized, Work_Model, City, Clicks
            ) VALUES (
                9999, 'AI Agent Development', 'Perplexity AI', 'Generative AI Systems Intern',
                'Remote', 'Yes', '2026-11-15', '2027-02-15', '$2,500 / month',
                'https://perplexity.ai/careers', 'Working on LLM agent search systems.',
                'Aggregator (Verified)', 'International', 'Paid', 'Remote', 'Remote', 0
            )
        """)
        conn.commit()

def test_company_careers_hub_route(seed_test_company):
    client = app.test_client()
    res = client.get("/company/perplexity-ai/careers")
    assert res.status_code == 200
    html = res.data.decode("utf-8")
    assert "Perplexity AI Careers" in html
    assert "application/ld+json" in html
    assert "Organization" in html
    assert "JobPosting" in html

def test_company_careers_hub_filtering(seed_test_company):
    client = app.test_client()
    res_all = client.get("/company/perplexity-ai/careers?type=all")
    assert res_all.status_code == 200
    res_intern = client.get("/company/perplexity-ai/careers?type=internship")
    assert res_intern.status_code == 200
    res_jobs = client.get("/company/perplexity-ai/careers?type=job")
    assert res_jobs.status_code == 200
