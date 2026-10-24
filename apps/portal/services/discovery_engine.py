"""
apps/portal/services/discovery_engine.py

Dynamic Internship Discovery & Multi-Domain Interleaving Engine.
Features:
- Recency scoring (newest first)
- Urgency scoring (end-date nearing within 3-14 days)
- India-first ranking
- Session-consistent dynamic jitter for fresh browsing without pagination drift
- Domain round-robin interleaving (solves domain clumping under "All Domains")
- Personalization: hides or badges already-applied posts; boosts student's enrolled domain
"""

from datetime import datetime, date
import re
from typing import List, Dict, Any, Optional, Set, Tuple

# All canonical track domains recognized by the portal
STANDARD_DOMAINS = [
    "AI Agent Development",
    "Full Stack Development",
    "Data Analyst",
    "Python Automation",
]

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
        # Check if country name is in region
        if any(k in reg for k in INDIA_KEYWORDS):
            return True
    loc = (item.get("location") or "").lower()
    title = (item.get("title") or "").lower()
    return any(k in loc or k in title for k in INDIA_KEYWORDS)


def compute_dynamic_score(
    item: Dict[str, Any],
    today: date,
    session_seed: int,
    user_domain: Optional[str] = None
) -> float:
    """
    Compute a composite discovery score for an opportunity:
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
        # Check comments / apply engagement on scraped leads
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
    - Divides candidate opportunities into domain buckets.
    - Each bucket is sorted by dynamic_score descending.
    - If user has a domain affinity, user domain gets an extra slot in the cycle.
    - Cycles through buckets in round-robin until all items are interleaved.
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
    # If user has a matching domain, interleave: [UserDomain, D2, UserDomain, D3, UserDomain, D4...]
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
        # Standard balanced 4-way round-robin
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

        # Every cycle, also take one from other_bucket if any
        if other_idx < len(other_bucket):
            interleaved.append(other_bucket[other_idx])
            other_idx += 1
            progress = True

        if not progress:
            break

    # Append any remaining items from any exhausted buckets
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
) -> Tuple[List[Dict[str, Any]], int]:
    """
    Main pipeline to filter, score, tag, and order all opportunities.
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
        candidates.append(p)

    # Process scraped leads
    for l in scraped_leads:
        lid = l.get("id")
        is_applied = lid in applied_leads
        l["is_applied"] = is_applied
        if hide_applied and is_applied:
            continue
        compute_dynamic_score(l, today, session_seed, user_domain)
        candidates.append(l)

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

    # Filter by duration if requested (1 month, 2 months, 3 months, 6 months)
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

    # If a specific domain was selected in the sidebar, filter strictly to it
    if active_domain:
        ad_lower = active_domain.strip().lower()
        filtered = [c for c in candidates if (c.get("domain") or "").strip().lower() == ad_lower]
        # Sort by dynamic_score DESC
        filtered.sort(key=lambda x: x.get("dynamic_score", 0), reverse=True)
        return filtered, len(filtered)

    # Under "All Domains": separate into India and International streams
    # Both streams are interleaved across domains to avoid domain clumping
    india_candidates = [c for c in candidates if c.get("region") == "india"]
    intl_candidates = [c for c in candidates if c.get("region") != "india"]

    # Interleave domains within India
    ordered_india = interleave_multi_domain(india_candidates, user_domain=user_domain)
    # Interleave domains within International
    ordered_intl = interleave_multi_domain(intl_candidates, user_domain=user_domain)

    # Final combined stream: India opportunities float first, followed by International
    final_stream = ordered_india + ordered_intl
    return final_stream, len(final_stream)
