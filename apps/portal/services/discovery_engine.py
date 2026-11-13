"""
apps/portal/services/discovery_engine.py

Next-Generation Opportunity Discovery & Multi-Signal "Best Fit" Recommendation Engine.
Features:
- 4-Pillar Best-Fit Algorithm (Track Domain 40%, CV Skills 30%, LMS Mastery 20%, Recency 10% + City/WFH Bonus)
- Skill-gap extraction & actionable LMS quiz completion nudges
- Recency & urgency scoring (end-date nearing within 3-14 days)
- India-first ranking
- Session-consistent dynamic jitter for fresh browsing without pagination drift
- Multi-domain round-robin interleaving (prevents domain clumping under "All Domains")
- Programmatic SEO support: Static chronological canonical feed for unauthenticated crawlers
"""

import json
import re
from datetime import datetime, date
from typing import List, Dict, Any, Optional, Set, Tuple

# All canonical track domains recognized by the portal
STANDARD_DOMAINS = [
    "AI Agent Development",
    "Full Stack Development",
    "Data Analyst",
    "Python Automation",
]

# Adjacent technical tracks that share transferable competencies
ADJACENT_DOMAINS = {
    "AI Agent Development": ["Python Automation", "Data Analyst"],
    "Python Automation": ["AI Agent Development", "Full Stack Development"],
    "Full Stack Development": ["Python Automation"],
    "Data Analyst": ["Python Automation", "AI Agent Development"],
}

# Domain skill taxonomy for skill matching and gap identification
DOMAIN_SKILLS_TAXONOMY = {
    "AI Agent Development": [
        "python", "langchain", "llm", "prompt engineering", "openai", "rag",
        "vector database", "pinecone", "chromadb", "fastapi", "transformers",
        "pytorch", "huggingface", "agents", "autogen", "crewai", "rest api", "git"
    ],
    "Full Stack Development": [
        "react", "javascript", "typescript", "node.js", "next.js", "express",
        "html", "css", "tailwind", "mongodb", "postgresql", "sql", "rest api",
        "redux", "docker", "git"
    ],
    "Data Analyst": [
        "python", "sql", "excel", "power bi", "tableau", "pandas", "numpy",
        "statistics", "data visualization", "exploratory data analysis",
        "data cleaning", "r", "reporting", "etl"
    ],
    "Python Automation": [
        "python", "selenium", "playwright", "beautifulsoup", "web scraping",
        "regex", "cron", "bash", "rest api", "pandas", "automation", "requests",
        "git", "ci/cd"
    ]
}

# All common tech keywords for token extraction (sorted longest first to match phrases)
ALL_TECH_KEYWORDS = sorted(
    list({skill for skills in DOMAIN_SKILLS_TAXONOMY.values() for skill in skills} | {
        "flask", "django", "aws", "gcp", "azure", "linux", "graphql", "redis",
        "c++", "java", "kubernetes", "tensorflow", "scikit-learn", "mysql"
    }),
    key=lambda x: -len(x)
)

INDIA_KEYWORDS = [
    "bangalore", "bengaluru", "delhi", "mumbai", "pune", "hyderabad",
    "kolkata", "chennai", "jaipur", "noida", "gurgaon", "gurugram",
    "ahmedabad", "chandigarh", "ncr", "india"
]


def parse_date_safe(val: Any) -> Optional[date]:
    """Parse a date string (YYYY-MM-DD...) or date object into date."""
    if not val:
        return None
    if isinstance(val, date):
        return val
    s = str(val).strip()[:10]
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def is_india_role(item: Dict[str, Any]) -> bool:
    """Check if opportunity is in India via region, location, or title."""
    reg = (item.get("region") or "").strip().lower()
    if reg == "india":
        return True
    if reg and reg != "international":
        if any(k in reg for k in INDIA_KEYWORDS):
            return True
    loc = (item.get("location") or "").lower()
    title = (item.get("title") or "").lower()
    return any(k in loc or k in title for k in INDIA_KEYWORDS)


def load_student_match_profile(conn, intern_id: Optional[int]) -> Optional[Dict[str, Any]]:
    """
    Extracts candidate signals from DB to power personalized 4-pillar matching:
    - Enrolled Track Domain (intern_accounts.domain)
    - Preferred City (intern_accounts.city)
    - Candidate Skills (cvs.skills_json / headline)
    - LMS Progress & Mastery (course_enrollments, day_quiz_attempts, gl_student_mastery, project_submissions)
    """
    if not intern_id or not conn:
        return None

    try:
        intern_row = conn.execute(
            "SELECT id, name, domain, city, tutor_completion_pct FROM intern_accounts WHERE id=?",
            (intern_id,)
        ).fetchone()
        if not intern_row:
            return None

        domain = intern_row["domain"] or ""
        city = (intern_row["city"] or "").strip().lower()

        # Load CV skills
        cv_skills: Set[str] = set()
        cv_row = conn.execute(
            "SELECT skills_json, headline, summary FROM cvs WHERE intern_id=? ORDER BY id DESC LIMIT 1",
            (intern_id,)
        ).fetchone()

        if cv_row:
            raw_skills = cv_row["skills_json"]
            if raw_skills:
                try:
                    parsed = json.loads(raw_skills)
                    if isinstance(parsed, list):
                        for s in parsed:
                            if isinstance(s, str) and s.strip():
                                cv_skills.add(s.strip().lower())
                    elif isinstance(parsed, dict):
                        for k, v in parsed.items():
                            if isinstance(v, list):
                                for s in v:
                                    cv_skills.add(str(s).strip().lower())
                except Exception:
                    for chunk in re.split(r"[,;|]+", raw_skills):
                        c = chunk.strip().lower()
                        if c:
                            cv_skills.add(c)
            # Also extract from headline/summary
            text_blob = f"{cv_row['headline'] or ''} {cv_row['summary'] or ''}".lower()
            for kw in ALL_TECH_KEYWORDS:
                if kw in text_blob:
                    cv_skills.add(kw)

        # Baseline skills from domain if CV is empty
        if not cv_skills and domain in DOMAIN_SKILLS_TAXONOMY:
            cv_skills = set(DOMAIN_SKILLS_TAXONOMY[domain][:6])

        # Compute LMS Mastery Score & Next Quiz Day
        lms_mastery_score = 40.0  # Base for registered intern
        next_quiz_day = 1

        # Check course enrollments
        enr_row = conn.execute(
            "SELECT id, current_day, completed_at FROM course_enrollments WHERE intern_id=? ORDER BY id DESC LIMIT 1",
            (intern_id,)
        ).fetchone()

        if enr_row:
            current_day = enr_row["current_day"] or 1
            next_quiz_day = max(1, current_day + 1)
            lms_mastery_score += min(30.0, current_day * 2.0)
            if enr_row["completed_at"]:
                lms_mastery_score += 20.0

            enr_id = enr_row["id"]
            # Passed quizzes
            try:
                quiz_count = conn.execute(
                    "SELECT COUNT(DISTINCT day_quiz_id) FROM day_quiz_attempts WHERE enrollment_id=? AND (passed=1 OR score >= 70)",
                    (enr_id,)
                ).fetchone()[0]
                lms_mastery_score += min(20.0, quiz_count * 5.0)
            except Exception:
                pass

        # Guided Learning concept mastery
        try:
            concept_count = conn.execute(
                "SELECT COUNT(*) FROM gl_student_mastery WHERE student_id=? AND mastery_level >= 3",
                (intern_id,)
            ).fetchone()[0]
            lms_mastery_score += min(15.0, concept_count * 3.0)
        except Exception:
            pass

        # Approved course projects
        try:
            proj_count = conn.execute(
                "SELECT COUNT(*) FROM project_submissions WHERE intern_id=? AND status='approved'",
                (intern_id,)
            ).fetchone()[0]
            lms_mastery_score += min(15.0, proj_count * 15.0)
        except Exception:
            pass

        lms_mastery_score = min(100.0, round(lms_mastery_score, 1))

        return {
            "intern_id": intern_id,
            "name": intern_row["name"],
            "domain": domain,
            "city": city,
            "cv_skills": cv_skills,
            "lms_mastery_score": lms_mastery_score,
            "next_quiz_day": next_quiz_day,
        }
    except Exception:
        return None


def extract_opportunity_skills(item: Dict[str, Any]) -> Set[str]:
    """Extract standard tech skill tokens from an opportunity's skills, title, or description."""
    skills: Set[str] = set()
    raw_skills = item.get("skills") or ""
    if raw_skills:
        for chunk in re.split(r"[,;|]+", raw_skills):
            c = chunk.strip().lower()
            if c:
                skills.add(c)

    text_blob = f"{item.get('title') or ''} {item.get('Role') or ''} {item.get('description') or ''} {item.get('Description') or ''}".lower()
    for kw in ALL_TECH_KEYWORDS:
        if re.search(r'\b' + re.escape(kw) + r'\b', text_blob):
            skills.add(kw)

    # Fallback to domain baseline if still empty
    dom = item.get("domain") or item.get("Domain") or ""
    if not skills and dom in DOMAIN_SKILLS_TAXONOMY:
        skills = set(DOMAIN_SKILLS_TAXONOMY[dom][:5])

    return skills


def calculate_best_fit_score(
    item: Dict[str, Any],
    student_profile: Dict[str, Any],
    today: date
) -> Dict[str, Any]:
    """
    Computes 4-Pillar Best Fit Score (0-99%) + Match Breakdown + Actionable LMS Nudge.
    Pillars:
    1. Track Domain Alignment (40%)
    2. CV Skills Overlap (30%)
    3. LMS Verified Mastery (20%)
    4. Recency & Urgency (10%)
    Bonus: +10-15 pts for City match or Work-from-Home
    """
    user_domain = student_profile.get("domain") or ""
    user_city = student_profile.get("city") or ""
    cv_skills = student_profile.get("cv_skills") or set()
    lms_mastery = student_profile.get("lms_mastery_score") or 40.0
    next_day = student_profile.get("next_quiz_day") or 1

    item_domain = item.get("domain") or item.get("Domain") or ""
    item_loc = (item.get("location") or item.get("Location") or item.get("City") or "").lower()
    work_mode = (item.get("work_mode") or item.get("Work_Model") or "").lower()
    is_remote = "remote" in work_mode or "remote" in item_loc or item.get("Is_Remote") == "Yes"

    # 1. Track Domain Alignment (40%)
    s_domain = 15.0
    if user_domain and item_domain:
        if user_domain.strip().lower() == item_domain.strip().lower():
            s_domain = 100.0
        elif item_domain in ADJACENT_DOMAINS.get(user_domain, []):
            s_domain = 55.0

    # 2. CV Skills Overlap (30%)
    job_skills = extract_opportunity_skills(item)
    matched_skills = sorted(list(cv_skills.intersection(job_skills)))
    missing_skills = sorted(list(job_skills - cv_skills))

    if job_skills:
        s_skills = min(100.0, (len(matched_skills) / max(1, min(len(job_skills), 5))) * 100.0)
    else:
        s_skills = 65.0

    # 3. LMS Verified Mastery (20%)
    s_mastery = float(lms_mastery)

    # 4. Freshness & Urgency (10%)
    pub_date = parse_date_safe(item.get("published_at") or item.get("Start_Date"))
    age_days = (today - pub_date).days if pub_date else 15
    if age_days <= 3:
        s_recency = 100.0
    elif age_days <= 7:
        s_recency = 80.0
    elif age_days <= 14:
        s_recency = 60.0
    elif age_days <= 30:
        s_recency = 40.0
    else:
        s_recency = 25.0

    end_date = parse_date_safe(item.get("End_Date") or item.get("expires_at"))
    if end_date:
        days_left = (end_date - today).days
        if 0 <= days_left <= 5:
            s_recency = min(100.0, s_recency + 20.0)

    # 5. City / WFH Additive Bonus
    s_bonus = 0.0
    if is_remote:
        s_bonus += 12.0
    elif user_city and user_city in item_loc:
        s_bonus += 15.0

    # Composite Score calculation
    raw_score = (
        0.40 * s_domain +
        0.30 * s_skills +
        0.20 * s_mastery +
        0.10 * s_recency +
        s_bonus
    )
    final_score = int(min(99, max(35, round(raw_score))))

    # Match Tier
    if final_score >= 85:
        match_tier = "Top Fit"
        badge_color = "emerald"
    elif final_score >= 70:
        match_tier = "Strong Fit"
        badge_color = "cyan"
    else:
        match_tier = "Moderate Fit"
        badge_color = "slate"

    # Actionable LMS Progression Nudge
    if missing_skills:
        first_missing = missing_skills[0].title()
        if matched_skills:
            top_matched = ", ".join(s.title() for s in matched_skills[:2])
            lms_nudge = f"Matched: {top_matched}. Complete Day {next_day} Quiz in {user_domain} to master {first_missing} and reach 95%+ Fit!"
        else:
            lms_nudge = f"Complete Day {next_day} Quiz in {user_domain} to build {first_missing} and boost your fit score!"
    else:
        lms_nudge = f"Verified profile match! You meet all core technical requirements for this {item_domain} role."

    return {
        "match_score": final_score,
        "match_tier": match_tier,
        "badge_color": badge_color,
        "matched_skills": [s.title() for s in matched_skills],
        "missing_skills": [s.title() for s in missing_skills],
        "lms_nudge": lms_nudge,
        "next_quiz_day": next_day,
    }


def compute_dynamic_score(
    item: Dict[str, Any],
    today: date,
    session_seed: int,
    user_domain: Optional[str] = None
) -> float:
    """
    Compute discovery score for catalogue sorting:
    - Base: India priority (+300 pts)
    - Recency: +10 to +100 pts based on days since published_at/Start_Date
    - Urgency: +15 to +60 pts based on days until End_Date
    - Personalization: +75 pts if matching intern's enrolled domain
    - Deterministic Jitter: +/- 15 pts based on session seed + item id
    """
    score = 0.0

    # 1. India priority
    in_india = is_india_role(item)
    item["region"] = "india" if in_india else "international"
    if in_india:
        score += 300.0

    # 2. Recency scoring (Start_Date or published_at)
    pub_date = parse_date_safe(item.get("published_at") or item.get("Start_Date"))
    if pub_date:
        age_days = (today - pub_date).days
        if age_days <= 1:
            score += 100.0
            item["is_new"] = True
        elif age_days <= 3:
            score += 80.0
            item["is_new"] = True
        elif age_days <= 7:
            score += 55.0
            item["is_new"] = False
        elif age_days <= 14:
            score += 35.0
            item["is_new"] = False
        elif age_days <= 30:
            score += 20.0
            item["is_new"] = False
        else:
            score += max(0.0, 10.0 - (age_days - 30) * 0.1)
            item["is_new"] = False
    else:
        item["is_new"] = False

    # 3. Urgency scoring (End_Date nearing)
    end_date = parse_date_safe(item.get("End_Date") or item.get("expires_at"))
    if end_date:
        days_left = (end_date - today).days
        if days_left < 0:
            item["is_closing_soon"] = False
        elif days_left <= 3:
            score += 60.0
            item["is_closing_soon"] = True
            item["days_left"] = days_left
        elif days_left <= 7:
            score += 40.0
            item["is_closing_soon"] = True
            item["days_left"] = days_left
        elif days_left <= 14:
            score += 20.0
            item["is_closing_soon"] = False
            item["days_left"] = days_left
        else:
            item["is_closing_soon"] = False
            item["days_left"] = days_left
    else:
        item["is_closing_soon"] = False

    # 4. Personal Domain Affinity
    domain = item.get("domain") or ""
    if user_domain and domain.strip().lower() == user_domain.strip().lower():
        score += 75.0
        item["is_for_you"] = True
    else:
        item["is_for_you"] = False

    # 5. Deterministic Session Jitter (stable across pagination for same session)
    item_id = item.get("id") or 0
    source_tag = item.get("source") or "lead"
    hash_str = f"{session_seed}_{source_tag}_{item_id}"
    jitter = (hash(hash_str) % 31) - 15  # -15 to +15 pts
    score += jitter

    item["dynamic_score"] = round(score, 2)
    return score


def get_applied_ids(conn, intern_id: Optional[int]) -> Tuple[Set[int], Set[int]]:
    """
    Get set of canonical post_ids and scraped job_ids applied by this intern.
    Returns: (applied_post_ids, applied_lead_ids)
    """
    if not intern_id:
        return set(), set()

    applied_posts = set()
    applied_leads = set()

    try:
        p_rows = conn.execute(
            "SELECT post_id FROM post_applications WHERE intern_id=?", (intern_id,)
        ).fetchall()
        applied_posts = {r[0] for r in p_rows if r[0] is not None}
    except Exception:
        pass

    try:
        l_rows = conn.execute(
            "SELECT job_id FROM scraped_internship_comments WHERE intern_id=?", (intern_id,)
        ).fetchall()
        applied_leads = {r[0] for r in l_rows if r[0] is not None}
    except Exception:
        pass

    return applied_posts, applied_leads


def interleave_multi_domain(
    items: List[Dict[str, Any]],
    user_domain: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Interleave opportunities across domains so that no single domain
    dominates consecutive results.
    """
    if not items:
        return []

    # Map items into buckets
    buckets: Dict[str, List[Dict[str, Any]]] = {}
    for dom in STANDARD_DOMAINS:
        buckets[dom] = []
    other_bucket: List[Dict[str, Any]] = []

    for it in items:
        dom = it.get("domain") or ""
        matched = False
        for std in STANDARD_DOMAINS:
            if dom.strip().lower() == std.lower():
                buckets[std].append(it)
                matched = True
                break
        if not matched:
            other_bucket.append(it)

    # Sort each bucket by dynamic_score DESC
    for b in buckets.values():
        b.sort(key=lambda x: x.get("dynamic_score", 0), reverse=True)
    other_bucket.sort(key=lambda x: x.get("dynamic_score", 0), reverse=True)

    # Build sequence cycle
    cycle_order: List[str] = []
    norm_user_dom = None
    if user_domain:
        for std in STANDARD_DOMAINS:
            if std.lower() == user_domain.strip().lower():
                norm_user_dom = std
                break

    if norm_user_dom and norm_user_dom in buckets:
        other_doms = [d for d in STANDARD_DOMAINS if d != norm_user_dom]
        for od in other_doms:
            cycle_order.append(norm_user_dom)
            cycle_order.append(od)
    else:
        cycle_order = list(STANDARD_DOMAINS)

    interleaved: List[Dict[str, Any]] = []
    bucket_indices = {d: 0 for d in STANDARD_DOMAINS}
    other_idx = 0

    total_items = len(items)
    while len(interleaved) < total_items:
        progress = False
        for dom in cycle_order:
            idx = bucket_indices[dom]
            bucket = buckets[dom]
            if idx < len(bucket):
                interleaved.append(bucket[idx])
                bucket_indices[dom] += 1
                progress = True

        if other_idx < len(other_bucket):
            interleaved.append(other_bucket[other_idx])
            other_idx += 1
            progress = True

        if not progress:
            break

    for dom in STANDARD_DOMAINS:
        idx = bucket_indices[dom]
        bucket = buckets[dom]
        if idx < len(bucket):
            interleaved.extend(bucket[idx:])
    if other_idx < len(other_bucket):
        interleaved.extend(other_bucket[other_idx:])

    return interleaved


def prepare_catalogue_stream(
    canonical_posts: List[Dict[str, Any]],
    scraped_leads: List[Dict[str, Any]],
    today: date,
    session_seed: int,
    user_domain: Optional[str] = None,
    student_profile: Optional[Dict[str, Any]] = None,
    active_tab: Optional[str] = None,
    applied_posts: Optional[Set[int]] = None,
    applied_leads: Optional[Set[int]] = None,
    hide_applied: bool = True,
    active_domain: Optional[str] = None,
    active_region: Optional[str] = None,
    search_q: Optional[str] = None,
    work_mode: Optional[str] = None,
    duration: Optional[str] = None,
    min_stipend: Optional[int] = None,
    max_age_days: Optional[int] = None,
    source_filter: Optional[str] = None,
) -> Tuple[List[Dict[str, Any]], int]:
    """
    Main pipeline to filter, score, tag, and order all opportunities.
    Supports authenticated 'Recommended for You' tab and cold-start static SEO feeds.
    Returns: (ordered_items, total_filtered_count)
    """
    applied_posts = applied_posts or set()
    applied_leads = applied_leads or set()

    candidates: List[Dict[str, Any]] = []

    # Process canonical posts
    for p in canonical_posts:
        pid = p.get("id")
        is_applied = pid in applied_posts
        p["is_applied"] = is_applied
        if hide_applied and is_applied:
            continue
        compute_dynamic_score(p, today, session_seed, user_domain)
        if student_profile:
            fit_data = calculate_best_fit_score(p, student_profile, today)
            p.update(fit_data)
        else:
            p["match_score"] = None
            p["match_tier"] = None
            p["badge_color"] = None
            p["matched_skills"] = []
            p["missing_skills"] = []
            p["lms_nudge"] = ""
        candidates.append(p)

    # Process scraped leads
    for l in scraped_leads:
        lid = l.get("id")
        is_applied = lid in applied_leads
        l["is_applied"] = is_applied
        if hide_applied and is_applied:
            continue
        compute_dynamic_score(l, today, session_seed, user_domain)
        if student_profile:
            fit_data = calculate_best_fit_score(l, student_profile, today)
            l.update(fit_data)
        else:
            l["match_score"] = None
            l["match_tier"] = None
            l["badge_color"] = None
            l["matched_skills"] = []
            l["missing_skills"] = []
            l["lms_nudge"] = ""
        candidates.append(l)

    # Filter by source if requested (portal vs curated)
    if source_filter:
        s_target = source_filter.strip().lower()
        if s_target in ("portal", "company", "direct", "post"):
            candidates = [c for c in candidates if c.get("source") == "post"]
        elif s_target in ("curated", "scraped", "lead", "leads"):
            candidates = [c for c in candidates if c.get("source") == "lead"]

    # Filter by region if requested
    if active_region:
        reg_target = active_region.strip().lower()
        candidates = [c for c in candidates if (c.get("region") or "").lower() == reg_target]

    # Filter by work mode if requested (remote, in-office, hybrid)
    if work_mode:
        wm_target = work_mode.strip().lower()
        if wm_target == "remote":
            candidates = [
                c for c in candidates
                if "remote" in (c.get("work_mode") or "").lower()
                or (c.get("location") or "").lower() == "remote"
            ]
        elif wm_target in ("in-office", "onsite", "on-site", "in office"):
            candidates = [
                c for c in candidates
                if any(w in (c.get("work_mode") or "").lower() for w in ("in-office", "in office", "onsite", "on-site"))
            ]
        elif wm_target == "hybrid":
            candidates = [
                c for c in candidates
                if "hybrid" in (c.get("work_mode") or "").lower()
            ]

    # Filter by duration if requested
    if duration:
        dur_target = duration.strip().lower().replace(" ", "").replace("months", "month")
        candidates = [
            c for c in candidates
            if dur_target in (c.get("duration") or "").lower().replace(" ", "").replace("months", "month")
        ]

    # Filter by min stipend if requested
    if min_stipend and min_stipend > 0:
        candidates = [
            c for c in candidates
            if not c.get("is_unpaid") and (c.get("stipend_max") or c.get("stipend_min") or 0) >= min_stipend
        ]

    # Filter by freshness (max age in days) if requested
    if max_age_days and max_age_days > 0:
        def _check_freshness(c):
            pdate = parse_date_safe(c.get("published_at") or c.get("Start_Date"))
            if not pdate:
                return True
            return (today - pdate).days <= max_age_days
        candidates = [c for c in candidates if _check_freshness(c)]

    # Filter by search query if requested
    if search_q:
        ql = search_q.strip().lower()
        candidates = [
            c for c in candidates
            if ql in (c.get("title") or "").lower()
            or ql in (c.get("company_name") or "").lower()
            or ql in (c.get("location") or "").lower()
            or ql in (c.get("domain") or "").lower()
        ]

    # Mode 1: Dedicated "Recommended for You" Tab
    if active_tab == "recommended" and student_profile:
        # Prioritize high-fit items: sort primarily by match_score DESC, then dynamic_score DESC
        candidates.sort(key=lambda x: (x.get("match_score") or 0, x.get("dynamic_score") or 0), reverse=True)
        return candidates, len(candidates)

    # Mode 2: Specific Domain filter
    if active_domain:
        ad_lower = active_domain.strip().lower()
        filtered = [c for c in candidates if (c.get("domain") or "").strip().lower() == ad_lower]
        if student_profile:
            filtered.sort(key=lambda x: (x.get("match_score") or 0, x.get("dynamic_score") or 0), reverse=True)
        else:
            filtered.sort(key=lambda x: x.get("dynamic_score", 0), reverse=True)
        return filtered, len(filtered)

    # Mode 3: "All Opportunities" / Canonical SEO Stream
    # Separate into India and International streams and interleave across domains
    india_candidates = [c for c in candidates if c.get("region") == "india"]
    intl_candidates = [c for c in candidates if c.get("region") != "india"]

    ordered_india = interleave_multi_domain(india_candidates, user_domain=user_domain)
    ordered_intl = interleave_multi_domain(intl_candidates, user_domain=user_domain)

    final_stream = ordered_india + ordered_intl
    return final_stream, len(final_stream)
