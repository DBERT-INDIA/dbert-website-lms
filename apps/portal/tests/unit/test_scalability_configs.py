import os
from datetime import datetime, timezone, timedelta
from config.financial_config import (
    get_financial_context,
    format_inr,
    CAUTION_DEPOSIT_INR,
    BALANCE_PAYABLE_INR
)
from config.institutional_config import (
    get_institutional_context,
    DIRECTOR_NAME,
    SOVEREIGN_DOMAIN
)
from services.cohort_calendar_service import get_next_cohort_standup, IST


def test_financial_config_values_and_formatting():
    ctx = get_financial_context()
    assert ctx["caution_deposit"] == CAUTION_DEPOSIT_INR
    assert ctx["balance_payable"] == BALANCE_PAYABLE_INR
    assert "₹" in ctx["caution_deposit_formatted"]
    assert "₹" in ctx["balance_payable_formatted"]
    assert ctx["upi_vpa"] == "Q652429146@ybl"
    assert format_inr(1500) == "₹1,500"


def test_institutional_config_mandates():
    ctx = get_institutional_context()
    assert ctx["director_name"] == DIRECTOR_NAME
    assert ctx["sovereign_domain"] == "https://dbert.in"
    assert "dbert.online" not in ctx["sovereign_domain"]


def test_cohort_calendar_calculates_monday_18_00_ist():
    # Test case 1: Saturday (e.g. Nov 14, 2026 21:00 IST) -> Next Monday Nov 16 18:00 IST
    sat = datetime(2026, 11, 14, 21, 0, 0, tzinfo=IST)
    standup = get_next_cohort_standup(sat)
    assert standup["batchStartDate"] == "2026-11-16T18:00:00+05:30"
    assert standup["batchStartDisplay"] == "Monday, 16 Nov 2026"
    assert standup["kickoffTimeDisplay"] == "06:00 PM IST"

    # Test case 2: Monday before 18:00 (e.g. Nov 16, 2026 10:00 IST) -> Today Nov 16 18:00 IST
    mon_morning = datetime(2026, 11, 16, 10, 0, 0, tzinfo=IST)
    standup_mon = get_next_cohort_standup(mon_morning)
    assert standup_mon["batchStartDate"] == "2026-11-16T18:00:00+05:30"
    assert standup_mon["batchStartDisplay"] == "Monday, 16 Nov 2026"

    # Test case 3: Monday after 18:00 (e.g. Nov 16, 2026 19:00 IST) -> Next Monday Nov 23 18:00 IST
    mon_evening = datetime(2026, 11, 16, 19, 0, 0, tzinfo=IST)
    standup_next = get_next_cohort_standup(mon_evening)
    assert standup_next["batchStartDate"] == "2026-11-23T18:00:00+05:30"
    assert standup_next["batchStartDisplay"] == "Monday, 23 Nov 2026"
