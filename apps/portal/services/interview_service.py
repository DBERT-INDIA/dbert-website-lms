"""
services/interview_service.py - AI Pre-Selection Interview Domain Service
Fulfills Phase 23 (Monolith Modularization) of INTERNSHIPPORTAL4_LOCAL_AI_AGENT_MASTER_PLAN.md

Encapsulates:
1. Static blueprint question bank assembly across domains.
2. Candidate attempt eligibility checking and cooling period calculation.
3. Interview attempt persistence and answer submission handling.
"""
import random
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

INTERVIEW_BLUEPRINT = [
    ("technical", 2), ("applied", 1), ("communication", 1),
]
INTERVIEW_DEFAULT_DOMAIN = "Python Automation"
INTERVIEW_DOMAIN_LABELS = {
    "AI Agent Development": "AI and agent development",
    "Data Analyst": "data analysis",
    "Full Stack Development": "web development",
    "Python Automation": "Python and automation",
    "UI/UX Design": "UI/UX and product design",
    "DevOps & Cloud": "DevOps and cloud infrastructure",
    "Mobile App Development": "mobile application development",
    "Cybersecurity": "cybersecurity and information security",
    "Digital Marketing": "digital marketing and growth",
}

INTERVIEW_DOMAIN_BANK = {
    "AI Agent Development": {
        "technical": [
            {"key": "ai_tech_01", "text": "In your own words, what is a large language model, and what does its 'context window' mean for building applications?"},
            {"key": "ai_tech_02", "text": "What is retrieval-augmented generation (RAG), and why might you use it instead of relying only on the model's built-in knowledge?"},
            {"key": "ai_tech_03", "text": "What's the difference between writing a good prompt and fine-tuning a model? When would you reach for each?"},
            {"key": "ai_tech_04", "text": "What are embeddings, and how are they useful when building an app that needs to search documents?"},
            {"key": "ai_tech_05", "text": "What does it mean for an AI agent to 'call a tool' or function, and why is that useful?"},
            {"key": "ai_tech_06", "text": "What is an LLM 'hallucination', and what are one or two practical ways to reduce it?"},
        ],
        "applied": [
            {"key": "ai_app_01", "text": "You're asked to build a support agent that answers questions from a company's PDF manuals. Outline the main steps you would take."},
            {"key": "ai_app_02", "text": "You need an agent that can read a user's email and book meetings on their calendar. How would you break that down?"},
            {"key": "ai_app_03", "text": "An AI feature you built sometimes gives confidently wrong answers. How would you investigate and improve it?"},
            {"key": "ai_app_04", "text": "You want to add a chatbot to a website that only answers questions about the product. How do you keep it on-topic?"},
        ],
        "communication": [
            {"key": "ai_comm_01", "text": "Explain, as you would to a non-technical friend, what an 'API key' is and why it must be kept secret."},
            {"key": "ai_comm_02", "text": "How would you explain to a customer, in plain language, why an AI assistant sometimes gets things wrong?"},
            {"key": "ai_comm_03", "text": "Explain what 'training data' is to someone who has never studied computer science."},
        ],
    },
    "Data Analyst": {
        "technical": [
            {"key": "da_tech_01", "text": "What is the difference between a SQL INNER JOIN and a LEFT JOIN? Give a simple example of when you'd use each."},
            {"key": "da_tech_02", "text": "How would you handle missing or null values in a dataset before analysis, and what trade-offs do your choices involve?"},
            {"key": "da_tech_03", "text": "What does GROUP BY do in SQL? Give an example of a question it helps you answer."},
            {"key": "da_tech_04", "text": "What is the difference between a primary key and a foreign key in a database?"},
            {"key": "da_tech_05", "text": "When would you use a bar chart versus a line chart versus a scatter plot to present data?"},
            {"key": "da_tech_06", "text": "What does it mean to 'clean' a dataset, and what are a few things you typically check for?"},
        ],
        "applied": [
            {"key": "da_app_01", "text": "Given a month of raw sales data, describe how you would find the top-performing products and present that insight to a manager."},
            {"key": "da_app_02", "text": "You receive a messy CSV of survey responses with inconsistent text and blanks. How do you make it analysis-ready?"},
            {"key": "da_app_03", "text": "A manager asks 'why did sales drop last week?' How would you approach answering that with data?"},
            {"key": "da_app_04", "text": "You're asked to build a simple weekly dashboard. What metrics would you include, and why?"},
        ],
        "communication": [
            {"key": "da_comm_01", "text": "Explain what a 'median' is and why it can be more useful than an 'average' in some situations, as if to someone new to data."},
            {"key": "da_comm_02", "text": "Explain the difference between correlation and causation to a manager, using a simple example."},
            {"key": "da_comm_03", "text": "How would you present a surprising finding to a team that expected the opposite result?"},
        ],
    },
    "Full Stack Development": {
        "technical": [
            {"key": "fs_tech_01", "text": "What happens, step by step, when a user types a URL into the browser and presses Enter?"},
            {"key": "fs_tech_02", "text": "What is the difference between client-side and server-side code? Give one example of work best done on each."},
            {"key": "fs_tech_03", "text": "What is the difference between a GET and a POST request, and when would you use each?"},
            {"key": "fs_tech_04", "text": "What is an API, and how does a front-end typically talk to a back-end?"},
            {"key": "fs_tech_05", "text": "What's the difference between a cookie, localStorage, and sessionStorage for keeping a user logged in?"},
            {"key": "fs_tech_06", "text": "What is a database, and why might you choose one over just storing data in files?"},
        ],
        "applied": [
            {"key": "fs_app_01", "text": "You need to build a simple to-do app where tasks persist after refresh. Describe the front-end, back-end, and storage pieces you'd use."},
            {"key": "fs_app_02", "text": "Design a login that keeps a user signed in across page refreshes. What pieces do you need?"},
            {"key": "fs_app_03", "text": "A page loads very slowly. How would you figure out why, and what would you try first?"},
            {"key": "fs_app_04", "text": "You're building a contact form that emails the team. Walk through what happens from submit to delivery."},
        ],
        "communication": [
            {"key": "fs_comm_01", "text": "Explain what an HTTP status code 404 vs 500 means, as you would to a teammate from a non-technical background."},
            {"key": "fs_comm_02", "text": "Explain what an 'API' is to someone who isn't a programmer."},
            {"key": "fs_comm_03", "text": "How would you explain to a client why their website needs both a front-end and a back-end?"},
        ],
    },
    "Python Automation": {
        "technical": [
            {"key": "py_tech_01", "text": "What is the difference between a list and a dictionary in Python, and when would you choose one over the other?"},
            {"key": "py_tech_02", "text": "How would you read a CSV file in Python and process each row? Mention any libraries you'd reach for."},
            {"key": "py_tech_03", "text": "What does try/except do in Python, and why is it important when automating tasks?"},
            {"key": "py_tech_04", "text": "What is a virtual environment, and why is it useful when working on Python projects?"},
            {"key": "py_tech_05", "text": "What is the difference between a list comprehension and a regular for-loop? When would you use each?"},
            {"key": "py_tech_06", "text": "What's the difference between a function and a variable, and why do we put code into functions?"},
        ],
        "applied": [
            {"key": "py_app_01", "text": "You're asked to automate renaming and sorting 500 files into folders by date. Describe your approach."},
            {"key": "py_app_02", "text": "You need to pull a daily report from a website and email it to your team automatically. How would you set that up?"},
            {"key": "py_app_03", "text": "A script you wrote works on your machine but fails on a colleague's. How would you track down why?"},
            {"key": "py_app_04", "text": "You want to fill out the same web form 100 times with data from a spreadsheet. How would you automate it?"},
        ],
        "communication": [
            {"key": "py_comm_01", "text": "Explain what a 'function' is and why we use them, as if teaching someone writing their first script."},
            {"key": "py_comm_02", "text": "Explain why hard-coding a password directly in a script is a bad idea, in plain terms."},
            {"key": "py_comm_03", "text": "How would you explain to a non-technical manager what 'automating a task' actually means?"},
        ],
    },
    "UI/UX Design": {
        "technical": [
            {"key": "ux_tech_01", "text": "What is the difference between UI and UX, and how do they collaborate in product development?"},
            {"key": "ux_tech_02", "text": "What are Figma Auto-Layout and Component Variants, and why are they essential for design systems?"},
            {"key": "ux_tech_03", "text": "What are WCAG accessibility guidelines, and what is the standard contrast ratio for normal text?"},
            {"key": "ux_tech_04", "text": "What is visual hierarchy, and what techniques do you use to guide user attention?"},
            {"key": "ux_tech_05", "text": "What are design tokens, and how do they bridge the gap between design and development?"},
            {"key": "ux_tech_06", "text": "What is the difference between low-fidelity wireframing and high-fidelity prototyping?"},
        ],
        "applied": [
            {"key": "ux_app_01", "text": "A client says their signup drop-off rate is 60%. Walk through how you would audit and redesign the onboarding flow."},
            {"key": "ux_app_02", "text": "How do you prepare design specs and assets in Figma for a frontend developer to minimize back-and-forth?"},
            {"key": "ux_app_03", "text": "You receive conflicting design feedback from two stakeholders. How do you resolve it objectively?"},
            {"key": "ux_app_04", "text": "How would you conduct a rapid 5-user usability test on a new prototype with zero budget?"},
        ],
        "communication": [
            {"key": "ux_comm_01", "text": "Explain what 'information architecture' means to a non-technical stakeholder."},
            {"key": "ux_comm_02", "text": "How would you advocate for user research when management wants to jump straight to visual design?"},
            {"key": "ux_comm_03", "text": "Explain why accessibility is important for business growth, not just compliance."},
        ],
    },
    "DevOps & Cloud": {
        "technical": [
            {"key": "do_tech_01", "text": "What is containerization, and how does Docker differ from a traditional virtual machine?"},
            {"key": "do_tech_02", "text": "What is a CI/CD pipeline, and what are the main stages from code commit to production release?"},
            {"key": "do_tech_03", "text": "What is the difference between a public and private subnet in AWS VPC architecture?"},
            {"key": "do_tech_04", "text": "What are Kubernetes Pods, Deployments, and Services, and how do they relate to each other?"},
            {"key": "do_tech_05", "text": "What is Infrastructure as Code (IaC), and what problems does Terraform solve?"},
            {"key": "do_tech_06", "text": "Why should secrets and credentials never be stored directly inside Docker images?"},
        ],
        "applied": [
            {"key": "do_app_01", "text": "A web service crashes under sudden traffic spikes. How would you diagnose CPU/memory bottlenecks and scale it?"},
            {"key": "do_app_02", "text": "Design a zero-downtime deployment strategy for a Flask/Node.js app behind Nginx."},
            {"key": "do_app_03", "text": "How would you set up automated alerts in Prometheus/Grafana if error rates exceed 5%?"},
            {"key": "do_app_04", "text": "You need to reduce Docker build times in GitHub Actions. What caching techniques would you apply?"},
        ],
        "communication": [
            {"key": "do_comm_01", "text": "Explain what 'the cloud' actually means to someone who has never worked in IT."},
            {"key": "do_comm_02", "text": "Explain why automated testing in CI pipelines saves developer time in the long run."},
            {"key": "do_comm_03", "text": "How would you explain the business impact of server uptime and SLA guarantees to leadership?"},
        ],
    },
    "Mobile App Development": {
        "technical": [
            {"key": "mob_tech_01", "text": "What is the difference between native development and cross-platform frameworks like React Native or Flutter?"},
            {"key": "mob_tech_02", "text": "How does React Native bridge or TurboModules communicate with native iOS/Android APIs?"},
            {"key": "mob_tech_03", "text": "Why is FlatList or virtualized list rendering essential for long lists on mobile devices?"},
            {"key": "mob_tech_04", "text": "What are safe area insets, and why must mobile layouts account for notches and home indicators?"},
            {"key": "mob_tech_05", "text": "How do you handle persistent offline state and local caching in a mobile app?"},
            {"key": "mob_tech_06", "text": "What is the difference between an Android APK and an Android App Bundle (AAB)?"},
        ],
        "applied": [
            {"key": "mob_app_01", "text": "A mobile screen stutters and drops below 60fps when scrolling. Walk through how you would profile and fix it."},
            {"key": "mob_app_02", "text": "Describe how you would implement optimistic updates for a social 'like' button on poor 3G network conditions."},
            {"key": "mob_app_03", "text": "How would you configure push notifications with Firebase Cloud Messaging (FCM) on both iOS and Android?"},
            {"key": "mob_app_04", "text": "An app crashes immediately upon launch on Android 14 only. How would you troubleshoot and resolve it?"},
        ],
        "communication": [
            {"key": "mob_comm_01", "text": "Explain to a client why Apple App Store review takes longer and has stricter rules than Google Play."},
            {"key": "mob_comm_02", "text": "Explain what 'offline-first' means and how it benefits mobile users with intermittent connectivity."},
            {"key": "mob_comm_03", "text": "How would you explain why an app cannot automatically access user location without explicit permission?"},
        ],
    },
    "Cybersecurity": {
        "technical": [
            {"key": "sec_tech_01", "text": "What is the CIA triad in information security, and what does each pillar represent?"},
            {"key": "sec_tech_02", "text": "Explain SQL Injection (SQLi) and Cross-Site Scripting (XSS), and how developers remediate each."},
            {"key": "sec_tech_03", "text": "What is the difference between symmetric and asymmetric encryption? Give an example of each."},
            {"key": "sec_tech_04", "text": "What does a Security Operations Center (SOC) analyst do when triaging a SIEM alert?"},
            {"key": "sec_tech_05", "text": "What is Broken Object Level Authorization (BOLA/IDOR), and why is it so prevalent in modern APIs?"},
            {"key": "sec_tech_06", "text": "What is defense-in-depth, and why is relying solely on a network firewall insufficient?"},
        ],
        "applied": [
            {"key": "sec_app_01", "text": "You discover an unauthenticated API endpoint exposing customer phone numbers. What immediate steps do you take?"},
            {"key": "sec_app_02", "text": "How would you conduct an internal phishing awareness simulation and measure organizational resilience?"},
            {"key": "sec_app_03", "text": "Describe the steps you would take during an active brute-force attack on a company's login endpoint."},
            {"key": "sec_app_04", "text": "You are auditing a web application with Burp Suite. Walk through your methodology for testing authentication flows."},
        ],
        "communication": [
            {"key": "sec_comm_01", "text": "Explain what multi-factor authentication (MFA) is and why SMS-based 2FA is less secure than authenticator apps."},
            {"key": "sec_comm_02", "text": "How would you explain a zero-day vulnerability to non-technical executive leadership?"},
            {"key": "sec_comm_03", "text": "Explain why security is a shared responsibility rather than solely the IT department's job."},
        ],
    },
    "Digital Marketing": {
        "technical": [
            {"key": "mkt_tech_01", "text": "What is the difference between on-page, off-page, and technical SEO?"},
            {"key": "mkt_tech_02", "text": "What are Google Core Web Vitals (LCP, INP, CLS), and how do they influence search engine rankings?"},
            {"key": "mkt_tech_03", "text": "In paid search campaigns, what is Quality Score, and how does it determine your actual cost-per-click?"},
            {"key": "mkt_tech_04", "text": "What is the Meta Pixel or Conversion API, and how does event deduplication work?"},
            {"key": "mkt_tech_05", "text": "What is the difference between first-touch, last-touch, and data-driven multi-touch attribution models?"},
            {"key": "mkt_tech_06", "text": "What are canonical tags in SEO, and how do they resolve duplicate content issues across URL parameters?"},
        ],
        "applied": [
            {"key": "mkt_app_01", "text": "A landing page has high traffic but only a 1.2% conversion rate. Walk through your strategy to optimize the funnel."},
            {"key": "mkt_app_02", "text": "You have a ₹50,000 monthly ad budget to launch a new B2B tech course. How do you allocate it across channels?"},
            {"key": "mkt_app_03", "text": "Describe how you would perform a competitor SEO gap analysis to discover untapped high-intent keywords."},
            {"key": "mkt_app_04", "text": "Your cost-per-acquisition (CPA) on Meta Ads doubled over two weeks. How do you diagnose ad fatigue and fix it?"},
        ],
        "communication": [
            {"key": "mkt_comm_01", "text": "Explain the difference between CAC (Customer Acquisition Cost) and LTV (Lifetime Value) to a founder."},
            {"key": "mkt_comm_02", "text": "Explain why SEO is a long-term compounding investment compared to paid ads which stop when budget ends."},
            {"key": "mkt_comm_03", "text": "How would you present a monthly marketing performance report showing ROI to a skeptical executive?"},
        ],
    },
}


class InterviewService:
    """Pre-selection AI interview domain service."""

    @staticmethod
    def assemble_questions(domain: str, exclude_keys: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Assembles questions from static bank preserving blueprint section balance."""
        exclude = set(exclude_keys or ())
        dom = domain if domain in INTERVIEW_DOMAIN_BANK else INTERVIEW_DEFAULT_DOMAIN
        field = INTERVIEW_DOMAIN_LABELS.get(dom, "this field")
        picked = []
        for section, count in INTERVIEW_BLUEPRINT:
            pool = INTERVIEW_DOMAIN_BANK[dom].get(section, [])
            avail = [q for q in pool if q["key"] not in exclude]
            if len(avail) < count:
                avail = list(pool)
            for q in random.sample(avail, min(count, len(avail))):
                picked.append((section, q))

        out = []
        for i, (section, q) in enumerate(picked, start=1):
            out.append({
                "id": i,
                "type": section,
                "key": q["key"],
                "text": q["text"].replace("{field}", field)
            })
        return out

    @staticmethod
    def check_eligibility(conn, intern_id: int, max_attempts: int = 2, cooling_hours: int = 24) -> Dict[str, Any]:
        """Checks if intern is eligible for a new interview attempt or in cooling period."""
        rows = conn.execute(
            """
            SELECT id, created_at, status 
            FROM preselection_interviews 
            WHERE intern_id = ? 
            ORDER BY id DESC
            """,
            (intern_id,)
        ).fetchall()
        total_attempts = len(rows)

        if total_attempts >= max_attempts:
            return {
                "eligible": False,
                "reason": "Max attempts reached",
                "total_attempts": total_attempts
            }

        if total_attempts > 0:
            last_attempt = rows[0]
            try:
                last_time = datetime.strptime(last_attempt["created_at"], "%Y-%m-%d %H:%M:%S")
                diff_hours = (datetime.now() - last_time).total_seconds() / 3600.0
                if diff_hours < cooling_hours:
                    return {
                        "eligible": False,
                        "reason": f"Cooling period active ({round(cooling_hours - diff_hours, 1)} hours remaining)",
                        "remaining_hours": round(cooling_hours - diff_hours, 1),
                        "total_attempts": total_attempts
                    }
            except Exception:
                pass

        return {
            "eligible": True,
            "total_attempts": total_attempts
        }
