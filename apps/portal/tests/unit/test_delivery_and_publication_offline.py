import sqlite3
from datetime import datetime, timezone

import pytest

from services.outbox_service import claim_outbox_batch, mark_event_sent, process_outbox_batch
from services.spotlight_schedule import admin_schedule, parse_window, spotlight_url_allowed, utc_timestamp


@pytest.fixture
def outbox(tmp_path):
    path = tmp_path / "outbox.db"
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript("""
        CREATE TABLE event_outbox (
            id INTEGER PRIMARY KEY, event_type TEXT, aggregate_type TEXT, aggregate_id TEXT,
            payload_json TEXT, status TEXT, retry_count INTEGER, max_retries INTEGER,
            next_retry_at TEXT, last_error TEXT, processed_at TEXT, created_at TEXT,
            updated_at TEXT, locked_by TEXT, lock_expires_at TEXT
        );
        INSERT INTO event_outbox VALUES
            (1, 'notice', 'learner', 'sample', '{}', 'PENDING', 0, 3, NULL, NULL, NULL, '2000-01-01', NULL, NULL, NULL);
    """)
    try:
        yield conn, path
    finally:
        conn.close()


def test_reclaimed_event_rejects_stale_lease(outbox):
    conn, _ = outbox
    first, = claim_outbox_batch(conn, worker_id="same-worker")
    conn.commit()
    assert claim_outbox_batch(conn, worker_id="another-worker") == []
    conn.execute("UPDATE event_outbox SET lock_expires_at = '2000-01-01'")
    conn.commit()
    replacement, = claim_outbox_batch(conn, worker_id="same-worker")
    assert replacement["locked_by"] != first["locked_by"]
    assert replacement["retry_count"] == 1
    assert not mark_event_sent(conn, 1, lease_token=first["locked_by"])
    assert mark_event_sent(conn, 1, lease_token=replacement["locked_by"])


def test_dispatcher_starts_only_after_claim_is_committed(outbox):
    conn, path = outbox

    def dispatcher(event_type, payload):
        with sqlite3.connect(path) as reader:
            assert reader.execute("SELECT status FROM event_outbox WHERE id=1").fetchone()[0] == "PROCESSING"
        return event_type == "notice" and payload == {}

    result = process_outbox_batch(conn, dispatcher)
    assert result["sent"] == 1
    assert conn.execute("SELECT status, locked_by FROM event_outbox").fetchone()["status"] == "SENT"


def test_spotlight_schedule_converts_and_classifies_ist_windows():
    start, end = parse_window("2026-11-23T14:00", "2026-11-23T16:00")
    assert start == "2026-11-23T08:30:00+00:00"
    assert end == "2026-11-23T10:30:00+00:00"
    row = {"publish_at": start, "expires_at": end, "is_active": 1}
    assert admin_schedule(row, utc_timestamp(datetime(2026, 11, 23, 8, tzinfo=timezone.utc)))["schedule_status"] == "Scheduled"
    assert admin_schedule(row, start) == {
        "schedule_status": "Live", "publish_at_ist": "2026-11-23T14:00", "expires_at_ist": "2026-11-23T16:00",
    }
    assert admin_schedule(row, end)["schedule_status"] == "Expired"
    assert admin_schedule({**row, "is_active": 0}, start)["schedule_status"] == "Paused"
    with pytest.raises(ValueError):
        parse_window("2026-11-23T16:00", "2026-11-23T14:00")
    assert spotlight_url_allowed("https://example.test/course")
    assert not spotlight_url_allowed("/internal/path")
