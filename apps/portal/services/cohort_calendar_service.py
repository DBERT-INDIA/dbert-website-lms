"""
services/cohort_calendar_service.py - Dynamic Rolling Cohort Calendar Engine

Eliminates hardcoded standup dates by computing the next weekly sprint cohort kickoff dynamically.
Standard Operating Rule: Cohorts kick off every Monday at 18:00:00 IST (UTC+05:30).
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, Any

# Indian Standard Time (UTC+05:30)
IST = timezone(timedelta(hours=5, minutes=30))


def get_next_cohort_standup(now: datetime = None) -> Dict[str, Any]:
    """
    Computes the upcoming cohort standup timestamp and formatted strings.
    If today is Monday before 18:00 IST, returns today at 18:00 IST.
    Otherwise, returns the upcoming Monday at 18:00 IST.
    """
    if now is None:
        now = datetime.now(IST)
    elif now.tzinfo is None:
        now = now.replace(tzinfo=IST)
    else:
        now = now.astimezone(IST)

    weekday = now.weekday()  # 0 = Monday, 6 = Sunday

    if weekday == 0 and (now.hour < 18 or (now.hour == 18 and now.minute == 0 and now.second == 0)):
        days_ahead = 0
    else:
        days_ahead = (7 - weekday) % 7
        if days_ahead == 0:
            days_ahead = 7

    target = (now + timedelta(days=days_ahead)).replace(hour=18, minute=0, second=0, microsecond=0)

    # Clean date display: e.g. 'Monday, 16 Nov 2026'
    display_str = f"{target.strftime('%A')}, {target.day} {target.strftime('%b %Y')}"

    return {
        "batchStartDate": target.isoformat(),
        "batchStartDisplay": display_str,
        "batchStartTimestamp": int(target.timestamp() * 1000),
        "kickoffTimeDisplay": "06:00 PM IST",
        "iso": target.isoformat(),
        "display": display_str,
    }
