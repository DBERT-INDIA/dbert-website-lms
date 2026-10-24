"""
generate_rich_jds.py
Generates clean, SEO-optimized, highly-relevant job descriptions
with About Company, About Role, Key Responsibilities, and Requirements
for all internships, processing Indian posts first.
"""
import sqlite3
import re
import html

DB_PATH = 'apps/portal/internship.db'

DOMAIN_SKILLS = {
    'AI Agent Development': [
        'Python', 'LangChain', 'LlamaIndex', 'OpenAI API', 'HuggingFace', 'FastAPI',
        'Prompt Engineering', 'RAG Pipelines', 'Vector Databases (Pinecone/Chroma)',
        'Agentic Workflows', 'Git', 'REST APIs'
    ],
    'Data Analyst': [
        'Python', 'SQL', 'Pandas', 'NumPy', 'PowerBI', 'Tableau', 'Excel (Advanced)',
        'Data Visualization', 'Statistical Analysis', 'ETL Pipelines', 'Metabase', 'Data Cleaning'
    ],
    'Full Stack Development': [
        'React.js', 'Next.js', 'Node.js', 'TypeScript', 'JavaScript', 'HTML5 & CSS3',
        'Tailwind CSS', 'RESTful APIs', 'PostgreSQL / MongoDB', 'Git & GitHub', 'Docker', 'State Management'
    ],
    'Python Automation': [
        'Python', 'Selenium', 'Playwright', 'BeautifulSoup', 'PyTest', 'Asyncio',
        'REST APIs', 'Bash Scripting', 'Task Automation', 'Git', 'Docker', 'Linux CLI'
    ]
}

RESPONSIBILITIES_TEMPLATES = {
    'AI Agent Development': [
        'Design, evaluate, and deploy autonomous AI agents and structured reasoning pipelines.',
        'Implement Retrieval-Augmented Generation (RAG) architecture using vector databases and embedding models.',
        'Collaborate with backend engineers to integrate LLM tool-calling APIs into core product workflows.',
        'Benchmark prompt variations, model outputs, and latency metrics to ensure high accuracy and response safety.',
        'Build structured unit tests and evaluation harnesses for LLM prompts and agent decision boundaries.',
        'Document technical workflows, schema definitions, and implementation guidelines for internal knowledge bases.'
    ],
    'Data Analyst': [
        'Extract, transform, and clean raw datasets from multiple operational sources and relational databases.',
        'Build high-impact interactive dashboards, KPI reports, and visual presentations using PowerBI and Tableau.',
        'Write optimized, modular SQL queries to uncover growth bottlenecks, user retention patterns, and operational efficiency.',
        'Partner with product and business stakeholders to translate strategic questions into actionable data insights.',
        'Perform cohort analysis, funnel tracking, and statistical hypothesis testing on product metrics.',
        'Maintain automated data hygiene checks and alert triggers for core metric anomalies.'
    ],
    'Full Stack Development': [
        'Develop responsive, accessible, and high-performance UI components using modern frontend frameworks.',
        'Design and consume scalable RESTful and GraphQL APIs backed by modular backend services.',
        'Write maintainable, well-tested code following clean architecture and continuous integration standards.',
        'Optimize database queries, indexing, and state management for low-latency user experiences.',
        'Participate in peer code reviews, sprint planning sessions, and architecture discussions.',
        'Diagnose and resolve cross-browser rendering bugs and server response performance issues.'
    ],
    'Python Automation': [
        'Architect and maintain automated scripting workflows that eliminate repetitive manual business operations.',
        'Build scalable web crawlers, data ingestion pipelines, and browser automation suites using Playwright/Selenium.',
        'Integrate external REST APIs, webhooks, and third-party SaaS services with custom Python utilities.',
        'Write robust error-handling, automated retry mechanisms, and structured logging routines.',
        'Create CI/CD test automation scripts and validation checks to improve software deployment reliability.',
        'Document script usage, environment variable setups, and scheduled cron executions.'
    ]
}

REQUIREMENTS_TEMPLATES = {
    'AI Agent Development': [
        'Strong foundational proficiency in Python programming and asynchronous coding patterns.',
        'Demonstrated hands-on experience or coursework with LLMs, prompt engineering, or framework libraries (e.g., LangChain, LlamaIndex).',
        'Familiarity with vector embeddings, similarity search, and API integrations.',
        'Proactive mindset, eager to experiment with modern AI architectures and solve unstructured problems.',
        'Pursuing or completed a Degree in Computer Science, Data Science, AI, or equivalent practical project experience.'
    ],
    'Data Analyst': [
        'Proficiency in SQL (joins, aggregations, window functions) and relational database concepts.',
        'Working experience with Python data science libraries (Pandas, NumPy, Matplotlib/Seaborn).',
        'Strong grasp of dashboard creation in business intelligence tools like PowerBI, Tableau, or Metabase.',
        'Curious analytical mindset with attention to detail and ability to synthesize data into clear recommendations.',
        'Pursuing or completed a Degree in Analytics, Statistics, Computer Science, Engineering, or a related discipline.'
    ],
    'Full Stack Development': [
        'Practical coding experience with modern JavaScript / TypeScript and frontend libraries (React, Next.js, or Vue).',
        'Understanding of backend technologies (Node.js, Python, or Go) and relational/NoSQL databases.',
        'Proficiency in version control using Git, branching models, and pull request workflows.',
        'Good understanding of web fundamentals: responsive CSS, semantic HTML, and HTTP lifecycle.',
        'Pursuing or completed a Degree in Computer Science, Software Engineering, or equivalent project portfolio.'
    ],
    'Python Automation': [
        'Solid programming skills in Python with knowledge of object-oriented and functional principles.',
        'Experience with web scraping or automation tools (Selenium, Playwright, BeautifulSoup, or Scrapy).',
        'Comfortable working with REST APIs, JSON data formats, and authentication tokens.',
        'Strong problem-solving instincts, debugging capabilities, and familiarity with Git and Linux environments.',
        'Pursuing or completed a Degree in IT, Computer Science, Engineering, or demonstrable personal automation scripts.'
    ]
}

def clean_text(s):
    if not s:
        return ""
    return re.sub(r'\s+', ' ', str(s)).strip()

def build_rich_jd(role, company, domain, location, work_model, region, stipend):
    domain = domain if domain in DOMAIN_SKILLS else 'Full Stack Development'
    role = clean_text(role) or f"{domain} Intern"
    company = clean_text(company) or "Leading Tech Organization"
    location = clean_text(location) or ("India" if region == 'India' else "Remote")
    work_model = clean_text(work_model) or ("Remote" if 'remote' in location.lower() else "Onsite")
    
    # 1. About Company
    if region == 'India':
        about_company = (
            f"<p><strong>{company}</strong> is a high-growth technology and innovation company operating in {location}, India. "
            f"Dedicated to delivering impactful digital solutions, the organization values agile execution, rapid product iteration, "
            f"and continuous learning. Interns collaborate directly with seasoned technical leaders, contributing to meaningful projects "
            f"that make a tangible impact across customer touchpoints and scalable systems.</p>"
        )
    else:
        about_company = (
            f"<p><strong>{company}</strong> is an innovative technology organization committed to engineering modern, scalable products. "
            f"With a collaborative distributed culture, the team empowers aspiring engineers and analysts to take ownership of real deliverables, "
            f"fostering accelerated professional growth through mentorship, code reviews, and industry best practices.</p>"
        )

    # 2. About Role
    about_role = (
        f"<p>We are seeking a proactive and driven <strong>{role}</strong> to join our {domain} team. "
        f"This opportunity is structured as a <strong>{work_model}</strong> position based out of <strong>{location}</strong>. "
        f"In this role, you will apply theoretical knowledge to production challenges, collaborate with cross-functional colleagues, "
        f"and help build reliable, performant solutions.</p>"
        f"<p>The selected candidate will receive structured guidance, participate in active sprint milestones, and gain end-to-end "
        f"exposure to modern development lifecycles, team standups, and codebase management.</p>"
    )

    # 3. Key Responsibilities
    resps = RESPONSIBILITIES_TEMPLATES.get(domain, RESPONSIBILITIES_TEMPLATES['Full Stack Development'])
    # Customize slightly with role name
    resp_items = [f"<li><span>{r}</span></li>" for r in resps]
    responsibilities_html = (
        f"<ul class=\"resp-list\">\n  " + "\n  ".join(resp_items) + "\n</ul>"
    )

    # 4. Requirements & Qualifications
    reqs = REQUIREMENTS_TEMPLATES.get(domain, REQUIREMENTS_TEMPLATES['Full Stack Development'])
    req_items = [f"<li><span>{rq}</span></li>" for rq in reqs]
    requirements_html = (
        f"<ul class=\"resp-list\">\n  " + "\n  ".join(req_items) + "\n</ul>"
    )

    # 5. Combined HTML Description
    full_html = (
        f"<div class=\"jd-section\">\n"
        f"  <h3 style=\"font-size:16px;font-weight:800;color:#0F172A;margin:0 0 10px;\">About {company}</h3>\n"
        f"  {about_company}\n"
        f"</div>\n\n"
        f"<div class=\"jd-section\" style=\"margin-top:20px;\">\n"
        f"  <h3 style=\"font-size:16px;font-weight:800;color:#0F172A;margin:0 0 10px;\">About the Role</h3>\n"
        f"  {about_role}\n"
        f"</div>\n\n"
        f"<div class=\"jd-section\" style=\"margin-top:20px;\">\n"
        f"  <h3 style=\"font-size:16px;font-weight:800;color:#0F172A;margin:0 10px 10px 0;\">Key Responsibilities</h3>\n"
        f"  {responsibilities_html}\n"
        f"</div>\n\n"
        f"<div class=\"jd-section\" style=\"margin-top:20px;\">\n"
        f"  <h3 style=\"font-size:16px;font-weight:800;color:#0F172A;margin:0 10px 10px 0;\">Requirements &amp; Qualifications</h3>\n"
        f"  {requirements_html}\n"
        f"</div>"
    )

    return full_html, resps, reqs

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Query all rows, prioritizing India first
    c.execute("""
        SELECT id, Role, Company, Domain, Location, Work_Model, Region, Stipend, Description
        FROM scraped_internships
        ORDER BY CASE WHEN Region = 'India' THEN 0 ELSE 1 END, id ASC
    """)
    rows = c.fetchall()
    print(f"Total rows fetched: {len(rows)}")

    updated_count = 0
    updates = []

    for r in rows:
        curr_desc = (r['Description'] or '').strip()
        # If it's a stub or too short or has awkward formatting
        needs_jd = (
            len(curr_desc) < 300 or
            curr_desc.startswith("Internshala Listing:") or
            "Location: RemoteAvailability:" in curr_desc or
            "WHO WE ARE" not in curr_desc and "About" not in curr_desc
        )

        if needs_jd:
            new_desc, resps, reqs = build_rich_jd(
                role=r['Role'],
                company=r['Company'],
                domain=r['Domain'],
                location=r['Location'],
                work_model=r['Work_Model'],
                region=r['Region'],
                stipend=r['Stipend']
            )
            updates.append((new_desc, r['id']))
            updated_count += 1

    print(f"Prepared {len(updates)} rich JDs. Applying updates to database...")
    c.executemany("UPDATE scraped_internships SET Description = ? WHERE id = ?", updates)
    conn.commit()
    conn.close()
    print(f"Successfully updated {updated_count} internships with rich, SEO-friendly Job Descriptions!")

if __name__ == '__main__':
    main()
