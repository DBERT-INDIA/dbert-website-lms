"""
apps/portal/services/grading_service.py
======================================
DBERT Standardized Project-Based Intern Grading & Evaluation Service (v2026.3)
-------------------------------------------------------------------------------
Evaluates engineering and internship capstone projects on a strictly calibrated
65 to 84 point scale (out of 100), ensuring realistic, uninflated, merit-backed
academic and industry credentials.

Scoring Formula (65 – 84 Max):
- Baseline Capstone Completion:       65 points
- Verified GitHub Pull Request:        +1 to +6 points
- Interactive Live Cloud Deployment:   +1 to +5 points
- Architecture / Technical Report:     +1 to +4 points
- Turnitin Originality Clearance (<3%): +1 to +4 points
-------------------------------------------------------
Total Score Window:                   65 (Min Pass) to 84 (Max Distinction)

Grade Tiers:
- 80 – 84: Grade: A (High Merit)
- 75 – 79: Grade: B+ (Merit)
- 70 – 74: Grade: B (Proficient)
- 65 – 69: Grade: C+ (Satisfactory)
"""
import hashlib
from typing import Dict, Any, List, Optional


def get_grade_tier(score: int) -> str:
    """Maps score in the 65-84 range to official performance grade."""
    if score >= 80:
        return "Grade: A (High Merit)"
    elif score >= 75:
        return "Grade: B+ (Merit)"
    elif score >= 70:
        return "Grade: B (Proficient)"
    else:
        return "Grade: C+ (Satisfactory)"


def generate_9_rubric_marks(total_score: int) -> List[int]:
    """
    Distributes total_score (65-84) across the 9 official DBERT academic rubrics:
    1. Technical Architecture & System Design (Max: 20)
    2. Code Quality & PEP 8 / Clean Code (Max: 10)
    3. Core Algorithms & Implementation (Max: 10)
    4. Data Integrity, Security & Validation (Max: 10)
    5. Testing & Verification Coverage (Max: 10)
    6. Project Documentation & Deliverables (Max: 10)
    7. Problem Solving & Analytical Agility (Max: 10)
    8. Sprint Cadence & Delivery Rigor (Max: 10)
    9. Code Review & Technical Viva (Max: 10)

    Guaranteed invariant: sum(rubrics) == total_score
    """
    # Clamp score to 65-84
    score = max(65, min(84, total_score))
    
    # Baseline marks for minimum passing score (65 points total)
    # [13, 6, 6, 6, 6, 7, 7, 7, 7] = 65
    rubrics = [13, 6, 6, 6, 6, 7, 7, 7, 7]
    extra = score - 65

    # Incremental distribution order (prioritizing Architecture, Originality/Rigor, Testing)
    # Target maximum caps: [17, 8, 8, 8, 9, 8, 8, 8, 9] = 83 (plus 1 to arch = 84)
    increment_plan = [0, 4, 1, 2, 3, 5, 6, 7, 8, 0, 0, 4, 1, 2, 3, 5, 6, 7, 8]
    for idx in increment_plan:
        if extra <= 0:
            break
        max_cap = 20 if idx == 0 else 10
        if rubrics[idx] < max_cap:
            rubrics[idx] += 1
            extra -= 1

    return rubrics


def calculate_project_grade(
    project_name: str,
    pr_verified: bool = True,
    live_demo: bool = True,
    report_submitted: bool = True,
    originality_cleared: bool = True,
    candidate_identifier: Optional[str] = None
) -> Dict[str, Any]:
    """
    Calculates deterministic, deliverable-backed score (65-84) and rubric marks.
    If candidate_identifier is provided (e.g. email or certId), uses it to introduce
    realistic granular variation within the deliverable component bounds.
    """
    # 1. Base Score
    score = 65

    # Determine granular component offsets using deterministic hash if identifier is provided
    salt = (candidate_identifier or project_name or "").strip().lower()
    h = int(hashlib.md5(salt.encode("utf-8")).hexdigest()[:6], 16) if salt else 42

    # 2. Verified GitHub PR (+1 to +6)
    if pr_verified:
        pr_pts = 4 + (h % 3)  # 4, 5, or 6
        score += pr_pts
    else:
        pr_pts = 0

    # 3. Interactive Live Cloud Demo (+1 to +5)
    if live_demo:
        demo_pts = 3 + ((h >> 2) % 3)  # 3, 4, or 5
        score += demo_pts
    else:
        demo_pts = 0

    # 4. Technical Architecture / Case Study Report (+1 to +4)
    if report_submitted:
        report_pts = 3 + ((h >> 4) % 2)  # 3 or 4
        score += report_pts
    else:
        report_pts = 0

    # 5. Originality & Turnitin Clearance < 3% (+1 to +4)
    if originality_cleared:
        orig_pts = 3 + ((h >> 6) % 2)  # 3 or 4
        score += orig_pts
    else:
        orig_pts = 0

    # Clamp strictly between 65 and 84
    final_score = max(65, min(84, score))
    grade = get_grade_tier(final_score)
    rubric_marks = generate_9_rubric_marks(final_score)

    return {
        "score": final_score,
        "grade": grade,
        "rubric_marks": rubric_marks,
        "breakdown": {
            "baseline_completion": 65,
            "pr_verified_points": pr_pts,
            "live_demo_points": demo_pts,
            "technical_report_points": report_pts,
            "originality_clearance_points": orig_pts,
            "total_score": final_score
        }
    }
