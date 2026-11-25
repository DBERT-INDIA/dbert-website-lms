"""Mentor availability, transactional seat reservations, and calendar exports."""

from datetime import datetime, time, timedelta, timezone
from urllib.parse import urlsplit


IST = timezone(timedelta(hours=5, minutes=30), "IST")

MENTOR_JOIN = """FROM mentor_availability_slots s
    LEFT JOIN staff_accounts st ON st.id = s.mentor_staff_id
    LEFT JOIN mentors m ON m.id = s.mentor_account_id"""
BOOKING_JOIN = MENTOR_JOIN + " JOIN mentor_session_bookings b ON b.slot_id = s.id"
BOOKING_FIELDS = """b.slot_id, s.start_time, s.end_time, s.topic, s.domain, s.agenda, s.follow_up, b.question,
    COALESCE(st.name, m.name, 'DBERT Mentor') AS mentor_name,
    COALESCE(s.meeting_link, b.meeting_link) AS meeting_link"""


class BookingError(ValueError):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


def ensure_mentor_schedule_schema(conn, ensure_column):
    for name, definition in (
        ("mentor_account_id", "INTEGER REFERENCES mentors(id)"),
        ("topic", "TEXT NOT NULL DEFAULT 'Technical Mentorship'"),
        ("domain", "TEXT NOT NULL DEFAULT 'All Tracks'"),
        ("capacity", "INTEGER NOT NULL DEFAULT 1"),
        ("seats_booked", "INTEGER NOT NULL DEFAULT 0"),
        ("meeting_link", "TEXT"),
        ("agenda", "TEXT"),
        ("follow_up", "TEXT"),
    ):
        ensure_column(conn, "mentor_availability_slots", name, definition)
    ensure_column(conn, "mentor_session_bookings", "question", "TEXT")

    if conn.dialect == "postgres":
        conn.execute("ALTER TABLE mentor_availability_slots ALTER COLUMN mentor_staff_id DROP NOT NULL")
        constraints = conn.execute(
            "SELECT conname FROM pg_constraint WHERE conrelid = 'mentor_session_bookings'::regclass "
            "AND contype = 'u' AND pg_get_constraintdef(oid) = 'UNIQUE (slot_id)'"
        ).fetchall()
        for row in constraints:
            identifier = row["conname"].replace('"', '""')
            conn.execute(f'ALTER TABLE mentor_session_bookings DROP CONSTRAINT IF EXISTS "{identifier}"')
    else:
        _upgrade_sqlite_slots(conn)

    conn.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_mentor_active_slot_intern "
        "ON mentor_session_bookings(slot_id, intern_id) WHERE status = 'booked'"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_mentor_account_slots "
        "ON mentor_availability_slots(mentor_account_id, start_time)"
    )


def _upgrade_sqlite_slots(conn):
    staff_required = any(
        row["name"] == "mentor_staff_id" and row["notnull"]
        for row in conn.execute("PRAGMA table_info(mentor_availability_slots)")
    )
    slot_only_unique = any(
        row["unique"] and [
            column["name"] for column in conn.execute("SELECT name FROM pragma_index_info(?)", (row["name"],))
        ] == ["slot_id"]
        for row in conn.execute("PRAGMA index_list(mentor_session_bookings)")
    )
    if not staff_required and not slot_only_unique:
        return

    conn.execute("SAVEPOINT mentor_schedule_upgrade")
    try:
        conn.execute("""
            CREATE TABLE mentor_availability_slots_upgrade (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mentor_staff_id INTEGER REFERENCES staff_accounts(id),
                mentor_account_id INTEGER REFERENCES mentors(id),
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                is_booked INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now','localtime')),
                topic TEXT NOT NULL DEFAULT 'Technical Mentorship',
                domain TEXT NOT NULL DEFAULT 'All Tracks',
                capacity INTEGER NOT NULL DEFAULT 1,
                seats_booked INTEGER NOT NULL DEFAULT 0,
                meeting_link TEXT,
                agenda TEXT,
                follow_up TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE mentor_session_bookings_upgrade (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slot_id INTEGER NOT NULL REFERENCES mentor_availability_slots_upgrade(id),
                intern_id INTEGER NOT NULL REFERENCES intern_accounts(id),
                meeting_link TEXT,
                status TEXT DEFAULT 'booked',
                created_at TEXT DEFAULT (datetime('now','localtime')),
                question TEXT
            )
        """)
        conn.execute("""
            INSERT INTO mentor_availability_slots_upgrade
                (id, mentor_staff_id, mentor_account_id, start_time, end_time, is_booked, created_at,
                 topic, domain, capacity, seats_booked, meeting_link, agenda, follow_up)
            SELECT id, mentor_staff_id, mentor_account_id, start_time, end_time, is_booked, created_at,
                   COALESCE(topic, 'Technical Mentorship'), COALESCE(domain, 'All Tracks'),
                   COALESCE(capacity, 1), COALESCE(seats_booked, 0), meeting_link, agenda, follow_up
            FROM mentor_availability_slots
        """)
        conn.execute("""
            INSERT INTO mentor_session_bookings_upgrade (id, slot_id, intern_id, meeting_link, status, created_at, question)
            SELECT id, slot_id, intern_id, meeting_link, status, created_at, question FROM mentor_session_bookings
        """)
        conn.execute("DROP TABLE mentor_session_bookings")
        conn.execute("DROP TABLE mentor_availability_slots")
        conn.execute("ALTER TABLE mentor_availability_slots_upgrade RENAME TO mentor_availability_slots")
        conn.execute("ALTER TABLE mentor_session_bookings_upgrade RENAME TO mentor_session_bookings")
        conn.execute("CREATE INDEX idx_mentor_slots ON mentor_availability_slots(mentor_staff_id, is_booked, start_time)")
        conn.execute("CREATE INDEX idx_mentor_bookings ON mentor_session_bookings(intern_id, status)")
    except Exception:
        conn.execute("ROLLBACK TO SAVEPOINT mentor_schedule_upgrade")
        raise
    finally:
        conn.execute("RELEASE SAVEPOINT mentor_schedule_upgrade")


def parse_slot_time(value):
    try:
        parsed = value if isinstance(value, datetime) else datetime.fromisoformat(value)
    except (TypeError, ValueError):
        raise BookingError("Enter a valid session date and time.") from None
    return parsed.astimezone(IST) if parsed.tzinfo else parsed.replace(tzinfo=IST)


def _stored_time(value):
    return value.astimezone(IST).strftime("%Y-%m-%d %H:%M:%S")


def schedule_now():
    return _stored_time(datetime.now(IST))


def confirmed_meeting_link(value):
    if not isinstance(value, str):
        return None
    value = value.strip()
    if not value or len(value) > 500 or any(letter.isspace() or ord(letter) < 32 for letter in value):
        return None
    try:
        url = urlsplit(value)
        if url.scheme != "https" or not url.hostname or url.username or url.password:
            return None
        if url.hostname == "meet.google.com" and url.path.startswith("/dbert-mentor-slot-"):
            return None
    except ValueError:
        return None
    return value


def create_slot(conn, *, staff_id, mentor_id, payload, domains):
    start = parse_slot_time(payload.get("start_time"))
    end = parse_slot_time(payload.get("end_time"))
    if start <= datetime.now(IST) or start >= end:
        raise BookingError("Choose a future start time and an end time after it.")
    if start.date() != end.date() or start.time() < time(14) or end.time() > time(20, 15):
        raise BookingError("Choose times within the 14:00–20:15 IST scheduling window.")

    domain = payload.get("domain") or "All Tracks"
    if domain not in ("All Tracks", *domains):
        raise BookingError("Choose a listed domain track.")
    topic = str(payload.get("topic") or "Technical Mentorship").strip()
    if not 1 <= len(topic) <= 120:
        raise BookingError("Enter a session topic of up to 120 characters.")
    try:
        capacity = int(str(payload.get("capacity", 1)))
    except (TypeError, ValueError):
        raise BookingError("Enter a capacity from 1 to 30.") from None
    if not 1 <= capacity <= 30:
        raise BookingError("Enter a capacity from 1 to 30.")
    supplied_link = payload.get("meeting_link")
    link = confirmed_meeting_link(supplied_link)
    if supplied_link and link is None:
        raise BookingError("Enter a valid HTTPS meeting link or leave it blank.")
    conn.execute(
        "INSERT INTO mentor_availability_slots "
        "(mentor_staff_id, mentor_account_id, start_time, end_time, topic, domain, capacity, meeting_link) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (staff_id, mentor_id, _stored_time(start), _stored_time(end), topic, domain, capacity, link),
    )


def _lock_booking(conn, intern_id, slot_id):
    if conn.dialect == "postgres":
        conn.execute("SELECT id FROM intern_accounts WHERE id = ? FOR UPDATE", (intern_id,)).fetchone()
        lock_clause = " FOR UPDATE"
    else:
        conn.execute("BEGIN IMMEDIATE")
        lock_clause = ""
    slot = conn.execute("SELECT * FROM mentor_availability_slots WHERE id = ?" + lock_clause, (slot_id,)).fetchone()
    if slot is None:
        raise BookingError("This session could not be found.", 404)
    return slot


def _booked_count(conn, slot_id):
    return conn.execute(
        "SELECT COUNT(*) AS total FROM mentor_session_bookings WHERE slot_id = ? AND status = 'booked'",
        (slot_id,),
    ).fetchone()["total"]


def _sync_capacity(conn, slot_id, count, capacity):
    conn.execute(
        "UPDATE mentor_availability_slots SET seats_booked = ?, is_booked = ? WHERE id = ?",
        (count, int(count >= (capacity or 1)), slot_id),
    )


def _record_notice(conn, intern_id, title, body):
    conn.execute(
        "INSERT INTO notifications (intern_id, kind, title, body, link) VALUES (?, 'mentorship', ?, ?, '/mentors/slots')",
        (intern_id, title, body),
    )


def reserve_slot(conn, *, intern_id, slot_id):
    slot = _lock_booking(conn, intern_id, slot_id)
    if parse_slot_time(slot["start_time"]) <= datetime.now(IST):
        raise BookingError("This session has already started.")
    existing = conn.execute(
        "SELECT b.slot_id FROM mentor_session_bookings b JOIN mentor_availability_slots s ON s.id = b.slot_id "
        "WHERE b.intern_id = ? AND b.status = 'booked' AND s.end_time > ? LIMIT 1",
        (intern_id, schedule_now()),
    ).fetchone()
    if existing:
        if existing["slot_id"] == slot_id:
            return confirmed_meeting_link(slot["meeting_link"])
        raise BookingError("Cancel or complete your upcoming reservation before booking another session.", 409)

    occupied = _booked_count(conn, slot_id)
    capacity = slot["capacity"] or 1
    if occupied >= capacity:
        raise BookingError("This session is full.", 409)
    link = confirmed_meeting_link(slot["meeting_link"])
    conn.execute(
        "INSERT INTO mentor_session_bookings (slot_id, intern_id, meeting_link, status) VALUES (?, ?, ?, 'booked')",
        (slot_id, intern_id, link),
    )
    _sync_capacity(conn, slot_id, occupied + 1, capacity)
    _record_notice(conn, intern_id, "Mentor Session Confirmed", "Your seat is reserved. View the session for joining details.")
    return link


def release_slot(conn, *, intern_id, slot_id):
    slot = _lock_booking(conn, intern_id, slot_id)
    if parse_slot_time(slot["start_time"]) <= datetime.now(IST):
        raise BookingError("This session has already started.")
    cancelled = conn.execute(
        "UPDATE mentor_session_bookings SET status = 'cancelled' "
        "WHERE slot_id = ? AND intern_id = ? AND status = 'booked'",
        (slot_id, intern_id),
    ).rowcount
    if not cancelled:
        raise BookingError("No active reservation found for this session.", 404)
    _sync_capacity(conn, slot_id, _booked_count(conn, slot_id), slot["capacity"])
    _record_notice(conn, intern_id, "Mentor Session Cancelled", "Your seat is available for another learner.")


def student_reservations(conn, intern_id, slot_id=None, *, past=False):
    period = "s.end_time <= ?" if past else "s.end_time > ?"
    order = " ORDER BY s.start_time DESC, s.id DESC LIMIT 10" if past else " ORDER BY s.start_time, s.id"
    filters = " WHERE b.intern_id = ? AND b.status = 'booked' AND " + period
    params = [intern_id, schedule_now()]
    if slot_id is not None:
        filters += " AND s.id = ?"
        params.append(slot_id)
    bookings = [dict(row) for row in conn.execute(
        "SELECT " + BOOKING_FIELDS + " " + BOOKING_JOIN + filters + order,
        params,
    )]
    for booking in bookings:
        booking["meeting_link"] = confirmed_meeting_link(booking["meeting_link"])
        booking["start_iso"] = parse_slot_time(booking["start_time"]).isoformat()
        booking["end_iso"] = parse_slot_time(booking["end_time"]).isoformat()
    return bookings


def student_calendar(conn, intern_id):
    slots = [dict(row) for row in conn.execute(
        "SELECT s.id, s.mentor_staff_id, s.mentor_account_id, s.start_time, s.end_time, s.topic, s.domain, "
        "s.capacity, COALESCE(st.name, m.name, 'DBERT Mentor') AS mentor_name, "
        "(SELECT COUNT(*) FROM mentor_session_bookings b WHERE b.slot_id = s.id AND b.status = 'booked') AS seats_booked, "
        "EXISTS(SELECT 1 FROM mentor_session_bookings b WHERE b.slot_id = s.id AND b.intern_id = ? "
        "AND b.status = 'booked') AS is_my_booking " + MENTOR_JOIN + " WHERE s.start_time > ? ORDER BY s.start_time, s.id",
        (intern_id, schedule_now()),
    )]
    mentors = {}
    for slot in slots:
        key = f"staff-{slot['mentor_staff_id']}" if slot["mentor_staff_id"] is not None else f"mentor-{slot['mentor_account_id']}"
        slot["mentor_id"] = key
        start = parse_slot_time(slot["start_time"])
        end = parse_slot_time(slot["end_time"])
        slot["start_iso"] = start.isoformat()
        slot["end_iso"] = end.isoformat()
        slot["booking_date"] = start.date().isoformat()
        slot["capacity"] = slot["capacity"] or 1
        mentor = mentors.setdefault(key, {"id": key, "name": slot["mentor_name"], "upcoming_count": 0})
        mentor["upcoming_count"] += 1
    return slots, list(mentors.values())


def _slot_owner(staff_id, mentor_id):
    return ("mentor_staff_id", staff_id) if staff_id is not None else ("mentor_account_id", mentor_id)


def owner_slots(conn, *, staff_id, mentor_id):
    owner_column, owner_id = _slot_owner(staff_id, mentor_id)
    slots = [dict(row) for row in conn.execute(
        f"SELECT * FROM mentor_availability_slots WHERE {owner_column} = ? ORDER BY start_time, id",
        (owner_id,),
    )]
    bookings = conn.execute(
        "SELECT b.slot_id, b.question, i.name AS intern_name, i.email AS intern_email "
        "FROM mentor_session_bookings b JOIN intern_accounts i ON i.id = b.intern_id "
        "JOIN mentor_availability_slots s ON s.id = b.slot_id "
        f"WHERE s.{owner_column} = ? AND b.status = 'booked' ORDER BY i.name, b.id",
        (owner_id,),
    )
    roster = {}
    for attendee in bookings:
        roster.setdefault(attendee["slot_id"], []).append(dict(attendee))
    for slot in slots:
        slot["attendees"] = roster.get(slot["id"], [])
        slot["seats_booked"] = len(slot["attendees"])
        slot["capacity"] = slot["capacity"] or 1
        slot["meeting_link"] = confirmed_meeting_link(slot["meeting_link"])
        start = parse_slot_time(slot["start_time"])
        end = parse_slot_time(slot["end_time"])
        slot["date_label"] = start.strftime("%Y-%m-%d")
        slot["time_label"] = f"{start:%H:%M} – {end:%H:%M}"
    return slots


def update_session_details(conn, *, staff_id, mentor_id, slot_id, agenda, follow_up, meeting_link):
    agenda, follow_up = agenda.strip(), follow_up.strip()
    if len(agenda) > 2000 or len(follow_up) > 2000:
        raise BookingError("Keep the agenda and follow-up under 2,000 characters each.")
    link = confirmed_meeting_link(meeting_link)
    if meeting_link.strip() and link is None:
        raise BookingError("Enter a valid HTTPS meeting link or leave it blank.")
    owner_column, owner_id = _slot_owner(staff_id, mentor_id)
    changed = conn.execute(
        "UPDATE mentor_availability_slots SET agenda = ?, follow_up = ?, meeting_link = ? "
        f"WHERE id = ? AND {owner_column} = ?",
        (agenda or None, follow_up or None, link, slot_id, owner_id),
    ).rowcount
    if not changed:
        raise BookingError("This session could not be found.", 404)
    conn.execute(
        "UPDATE mentor_session_bookings SET meeting_link = ? WHERE slot_id = ? AND status = 'booked'",
        (link, slot_id),
    )


def update_learner_question(conn, *, intern_id, slot_id, question):
    question = question.strip()
    if len(question) > 600:
        raise BookingError("Keep your question under 600 characters.")
    changed = conn.execute(
        "UPDATE mentor_session_bookings SET question = ? "
        "WHERE slot_id = ? AND intern_id = ? AND status = 'booked' "
        "AND slot_id IN (SELECT id FROM mentor_availability_slots WHERE start_time > ?)",
        (question or None, slot_id, intern_id, schedule_now()),
    ).rowcount
    if not changed:
        raise BookingError("Choose an upcoming session you have reserved.", 404)


def _calendar_text(value):
    return str(value or "").replace("\\", "\\\\").replace("\r\n", "\n").replace("\r", "\n").replace("\n", "\\n").replace(";", "\\;").replace(",", "\\,")


def _calendar_line(line):
    parts, current, size = [], "", 0
    for character in line:
        length = len(character.encode("utf-8"))
        if size + length > 75:
            parts.append(current)
            current, size = " ", 1
        current += character
        size += length
    return "\r\n".join([*parts, current])


def session_calendar(booking):
    def stamp(value):
        return parse_slot_time(value).astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    lines = [
        "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//DBERT//Mentor Schedule//EN", "BEGIN:VEVENT",
        f"UID:mentor-slot-{booking['slot_id']}@dbert.in",
        f"DTSTAMP:{stamp(datetime.now(timezone.utc))}",
        f"DTSTART:{stamp(booking['start_time'])}",
        f"DTEND:{stamp(booking['end_time'])}",
        f"SUMMARY:{_calendar_text(booking['topic'])}",
        f"DESCRIPTION:{_calendar_text('DBERT mentorship with ' + (booking['mentor_name'] or 'your mentor'))}",
    ]
    link = confirmed_meeting_link(booking.get("meeting_link"))
    if link:
        lines.append(f"URL:{link}")
    return "\r\n".join(map(_calendar_line, [*lines, "END:VEVENT", "END:VCALENDAR", ""]))
