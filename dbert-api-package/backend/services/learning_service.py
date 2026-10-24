from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

def grade_quiz_submission(submitted_answers: Dict[str, Any], answer_key: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate quiz score percentage and pass/fail status."""
    total_questions = len(answer_key)
    if total_questions == 0:
        return {"score": 100.0, "passed": True, "correct_count": 0, "total": 0}

    correct_count = 0
    for q_id, correct_ans in answer_key.items():
        if submitted_answers.get(str(q_id)) == correct_ans:
            correct_count += 1

    score_pct = (correct_count / total_questions) * 100.0
    passed = score_pct >= 70.0
    return {
        "score": round(score_pct, 2),
        "passed": passed,
        "correct_count": correct_count,
        "total": total_questions
    }

async def generate_socratic_tutor_response(subtopic_title: str, user_message: str, history: List[Dict[str, str]]) -> str:
    """Generate interactive socratic tutoring guidance without giving away answers."""
    # Socratic response template
    return (
        f"Regarding '{subtopic_title}': That is a thoughtful perspective! "
        f"Consider what happens when input parameters edge out of expected bounds. "
        f"How would you ensure resilience in that specific scenario?"
    )
