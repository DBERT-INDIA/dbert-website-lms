import json
import datetime
import uuid
from typing import Optional, Dict, Any, List, Union, Callable

# -----------------------------------------------------------------------------
# PHASE 14 — Transactional Event Outbox Service
# Master Plan: INTERNSHIPPORTAL4_LOCAL_AI_AGENT_MASTER_PLAN.md (§23)
# -----------------------------------------------------------------------------

# Supported Event Types
EVENT_APPLICATION_SUBMITTED = "application.submitted"
EVENT_APPLICATION_SELECTED  = "application.selected"
EVENT_APPLICATION_REJECTED  = "application.rejected"
EVENT_ENROLLMENT_CREATED    = "enrollment.created"
EVENT_PAYMENT_SUBMITTED     = "payment.submitted"
EVENT_PAYMENT_ACCEPTED      = "payment.accepted"
EVENT_PAYMENT_REJECTED      = "payment.rejected"
EVENT_MENTOR_ASSIGNED       = "mentor.assigned"
EVENT_TASK_ASSIGNED         = "task.assigned"
EVENT_TASK_REVIEWED         = "task.reviewed"
EVENT_CERTIFICATE_ISSUED    = "certificate.issued"

ALL_OUTBOX_EVENTS = {
    EVENT_APPLICATION_SUBMITTED,
    EVENT_APPLICATION_SELECTED,
    EVENT_APPLICATION_REJECTED,
    EVENT_ENROLLMENT_CREATED,
    EVENT_PAYMENT_SUBMITTED,
    EVENT_PAYMENT_ACCEPTED,
    EVENT_PAYMENT_REJECTED,
    EVENT_MENTOR_ASSIGNED,
    EVENT_TASK_ASSIGNED,
    EVENT_TASK_REVIEWED,
    EVENT_CERTIFICATE_ISSUED,
}

# Notification / Outbox States
STATUS_PENDING     = "PENDING"
STATUS_SENT        = "SENT"
STATUS_FAILED      = "FAILED"
STATUS_RETRYING    = "RETRYING"
STATUS_DEAD_LETTER = "DEAD_LETTER"
STATUS_PROCESSING  = "PROCESSING"

ALL_OUTBOX_STATUSES = {
    STATUS_PENDING,
    STATUS_SENT,
    STATUS_FAILED,
    STATUS_RETRYING,
    STATUS_DEAD_LETTER,
    STATUS_PROCESSING,
}


def _now_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def enqueue_outbox_event(
    conn,
    event_type: str,
    aggregate_type: str,
    aggregate_id: Union[int, str],
    payload: Dict[str, Any],
    max_retries: int = 3
) -> int:
    """
    Enqueues an outbox event inside the active database transaction.
    Atomic with business logic — if the transaction rolls back, this event rolls back.
    """
    if event_type not in ALL_OUTBOX_EVENTS:
        raise ValueError(f"Unknown outbox event type: '{event_type}'. Must be one of {ALL_OUTBOX_EVENTS}")

    payload_json = json.dumps(payload, default=str)
    now = _now_str()

    cur = conn.execute(
        """
        INSERT INTO event_outbox (
            event_type, aggregate_type, aggregate_id, payload_json,
            status, retry_count, max_retries, next_retry_at,
            created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, 0, ?, ?, ?, ?)
        """,
        (
            event_type,
            aggregate_type,
            str(aggregate_id),
            payload_json,
            STATUS_PENDING,
            max_retries,
            now,
            now,
            now
        )
    )
    return cur.lastrowid or getattr(conn, "lastrowid", None) or getattr(conn, "_last_rowid", None) or 0


def reclaim_expired_leases(conn) -> int:
    """Count an expired processing lease as an interrupted delivery attempt."""
    now = _now_str()
    cur = conn.execute(
        """
        UPDATE event_outbox
        SET status = CASE WHEN retry_count + 1 >= max_retries THEN ? ELSE ? END,
            next_retry_at = CASE WHEN retry_count + 1 >= max_retries THEN NULL ELSE ? END,
            retry_count = retry_count + 1, last_error = 'Delivery worker lease expired.',
            locked_by = NULL, lock_expires_at = NULL, updated_at = ?
        WHERE status = ? AND (lock_expires_at IS NULL OR lock_expires_at <= ?)
        """,
        (STATUS_DEAD_LETTER, STATUS_RETRYING, now, now, STATUS_PROCESSING, now)
    )
    return cur.rowcount if hasattr(cur, "rowcount") else 0


def claim_outbox_batch(
    conn,
    worker_id: str = "worker_default",
    limit: int = 50,
    lease_seconds: int = 300
) -> List[Dict[str, Any]]:
    """
    Claim up to the requested number of eligible events under one unique lease.
    """
    reclaim_expired_leases(conn)
    now = datetime.datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    expires_str = (now + datetime.timedelta(seconds=max(1, lease_seconds))).strftime("%Y-%m-%d %H:%M:%S")
    lease_token = f"{worker_id}:{uuid.uuid4().hex}"
    row_lock = " FOR UPDATE SKIP LOCKED" if getattr(conn, "dialect", "") == "postgres" else ""
    eligibility = "status IN (?, ?) AND (next_retry_at IS NULL OR next_retry_at <= ?)"
    ready = (STATUS_PENDING, STATUS_RETRYING, now_str)
    conn.execute(
        f"""
        UPDATE event_outbox
        SET status = ?, locked_by = ?, lock_expires_at = ?, updated_at = ?
        WHERE id IN (
            SELECT id FROM event_outbox WHERE {eligibility} ORDER BY id LIMIT ?{row_lock}
        ) AND {eligibility}
        """,
        (STATUS_PROCESSING, lease_token, expires_str, now_str, *ready, max(0, limit), *ready),
    )
    rows = conn.execute(
        """
        SELECT id, event_type, aggregate_type, aggregate_id, payload_json,
               status, retry_count, max_retries, next_retry_at, last_error, created_at,
               locked_by, lock_expires_at
        FROM event_outbox
        WHERE locked_by=?
        ORDER BY id
        """,
        (lease_token,),
    ).fetchall()

    claimed = []
    for r in rows:
        item = dict(r)
        try:
            item["payload"] = json.loads(item.get("payload_json") or "{}")
        except Exception:
            item["payload"] = {}
        claimed.append(item)

    return claimed


def fetch_pending_outbox_events(conn, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Fetches up to `limit` outbox events that are eligible for processing:
    status is 'PENDING' or 'RETRYING', and next_retry_at <= now.
    """
    return claim_outbox_batch(conn, worker_id="fetch_worker", limit=limit)


def _owned_event(event_id, lease_token, now):
    if lease_token is not None:
        return (
            "id=? AND status=? AND locked_by=? AND lock_expires_at>?",
            (event_id, STATUS_PROCESSING, lease_token, now),
        )
    # Preserve management calls for idle events. A live worker must prove ownership.
    return "id=? AND status IN (?, ?) AND locked_by IS NULL", (event_id, STATUS_PENDING, STATUS_RETRYING)


def mark_event_sent(conn, event_id: int, *, lease_token: Optional[str] = None) -> bool:
    """Record delivery only while the caller owns the current lease."""
    now = _now_str()
    predicate, params = _owned_event(event_id, lease_token, now)
    cur = conn.execute(
        f"""
        UPDATE event_outbox
        SET status = ?, processed_at = ?, updated_at = ?, last_error = NULL, locked_by = NULL, lock_expires_at = NULL
        WHERE {predicate}
        """,
        (STATUS_SENT, now, now, *params)
    )
    return cur.rowcount > 0


def mark_event_failed(
    conn,
    event_id: int,
    error_message: str,
    base_backoff_seconds: int = 30,
    *,
    lease_token: Optional[str] = None,
) -> str:
    """
    Marks an outbox event as failed. Computes exponential backoff.
    Transitions to RETRYING if retry_count < max_retries, otherwise DEAD_LETTER.
    Releases worker lease. Returns the new status.
    """
    now = datetime.datetime.now()
    now_text = now.strftime("%Y-%m-%d %H:%M:%S")
    predicate, params = _owned_event(event_id, lease_token, now_text)
    row = conn.execute(
        f"SELECT retry_count, max_retries FROM event_outbox WHERE {predicate}", params,
    ).fetchone()
    if not row:
        return STATUS_FAILED

    new_retry_count = row["retry_count"] + 1
    max_retries = row["max_retries"]

    if new_retry_count >= max_retries:
        new_status = STATUS_DEAD_LETTER
        next_retry_str = None
    else:
        new_status = STATUS_RETRYING
        # Exponential backoff: 2^(retry_count) * base_backoff_seconds
        backoff_sec = min((2 ** min(new_retry_count, 12)) * max(0, base_backoff_seconds), 86400)
        next_retry_str = (now + datetime.timedelta(seconds=backoff_sec)).strftime("%Y-%m-%d %H:%M:%S")

    updated = conn.execute(
        f"""
        UPDATE event_outbox
        SET status = ?, retry_count = ?, next_retry_at = ?, last_error = ?, updated_at = ?, locked_by = NULL, lock_expires_at = NULL
        WHERE {predicate} AND retry_count=?
        """,
        (new_status, new_retry_count, next_retry_str, error_message[:1000], now_text, *params, row["retry_count"])
    )
    return new_status if updated.rowcount == 1 else STATUS_FAILED


def _renew_outbox_lease(conn, event_id, lease_token, lease_seconds):
    now = datetime.datetime.now()
    now_text = now.strftime("%Y-%m-%d %H:%M:%S")
    expires = (now + datetime.timedelta(seconds=lease_seconds)).strftime("%Y-%m-%d %H:%M:%S")
    predicate, params = _owned_event(event_id, lease_token, now_text)
    updated = conn.execute(
        f"UPDATE event_outbox SET lock_expires_at=? WHERE {predicate}", (expires, *params),
    )
    return updated.rowcount == 1


def process_outbox_batch(
    conn,
    dispatcher_func: Callable[[str, Dict[str, Any]], bool],
    batch_size: int = 50,
    base_backoff_seconds: int = 30,
) -> Dict[str, int]:
    """
    Processes claims outside worker transactions and checkpoints each acknowledgement.
    Use a dedicated worker connection, because delivery commits the leases it acquires.
    """
    lease_seconds = 300
    events = claim_outbox_batch(conn, worker_id="dispatch", limit=batch_size, lease_seconds=lease_seconds)
    conn.commit()
    metrics = {
        "processed": 0,
        "sent": 0,
        "retrying": 0,
        "dead_letter": 0,
        "lost_lease": 0,
    }

    for ev in events:
        event_id = ev["id"]
        lease_token = ev["locked_by"]
        owned = _renew_outbox_lease(conn, event_id, lease_token, lease_seconds)
        conn.commit()
        if not owned:
            metrics["lost_lease"] += 1
            continue

        metrics["processed"] += 1
        reason = "Dispatcher returned non-success result."
        try:
            delivered = dispatcher_func(ev["event_type"], ev["payload"])
        except Exception as error:
            delivered = False
            reason = str(error)

        if delivered:
            if mark_event_sent(conn, event_id, lease_token=lease_token):
                metrics["sent"] += 1
            else:
                metrics["lost_lease"] += 1
        else:
            status = mark_event_failed(conn, event_id, reason, base_backoff_seconds, lease_token=lease_token)
            if status == STATUS_RETRYING:
                metrics["retrying"] += 1
            elif status == STATUS_DEAD_LETTER:
                metrics["dead_letter"] += 1
            else:
                metrics["lost_lease"] += 1
        conn.commit()

    return metrics


def replay_dead_letters(conn, event_ids: Optional[List[int]] = None) -> int:
    """
    Resets DEAD_LETTER events to PENDING with reset retry count and immediate next_retry_at.
    If event_ids is provided, resets only those; otherwise resets all DEAD_LETTER events.
    """
    now = _now_str()
    if event_ids:
        placeholders = ",".join("?" for _ in event_ids)
        cur = conn.execute(
            f"""
            UPDATE event_outbox
            SET status = ?, retry_count = 0, next_retry_at = ?, last_error = NULL, updated_at = ?
            WHERE status = ? AND id IN ({placeholders})
            """,  # nosec B608
            (STATUS_PENDING, now, now, STATUS_DEAD_LETTER, *event_ids)
        )
    else:
        cur = conn.execute(
            """
            UPDATE event_outbox
            SET status = ?, retry_count = 0, next_retry_at = ?, last_error = NULL, updated_at = ?
            WHERE status = ?
            """,
            (STATUS_PENDING, now, now, STATUS_DEAD_LETTER)
        )
    return cur.rowcount
