"""Publication windows for ecosystem announcements."""

from datetime import datetime, timedelta, timezone
from urllib.parse import urlsplit


INDIA_TIME = timezone(timedelta(hours=5, minutes=30))


def utc_timestamp(value):
    return value.astimezone(timezone.utc).isoformat(timespec="seconds")


def parse_window(start, end):
    def from_form(value):
        if not value:
            return None
        try:
            local = datetime.strptime(value, "%Y-%m-%dT%H:%M").replace(tzinfo=INDIA_TIME)
        except (TypeError, ValueError):
            raise ValueError("Enter publication times in the IST date and time fields.") from None
        return utc_timestamp(local)

    start, end = from_form(start), from_form(end)
    if start and end and end <= start:
        raise ValueError("The expiry time must be after the publish time.")
    return start, end


def spotlight_url_allowed(url):
    try:
        parsed = urlsplit(url)
        return parsed.scheme == "https" and bool(parsed.hostname) and parsed.username is None and parsed.password is None
    except ValueError:
        return False


def admin_schedule(row, now):
    start, end = row.get("publish_at"), row.get("expires_at")
    to_local = lambda value: datetime.fromisoformat(value).astimezone(INDIA_TIME).strftime("%Y-%m-%dT%H:%M") if value else ""
    if not row["is_active"]:
        status = "Paused"
    elif end and now >= end:
        status = "Expired"
    elif start and now < start:
        status = "Scheduled"
    else:
        status = "Live"
    return {"publish_at_ist": to_local(start), "expires_at_ist": to_local(end), "schedule_status": status}
