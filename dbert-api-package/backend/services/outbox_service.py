import json
from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from backend.models.admin import EventOutbox

async def queue_event(
    db: AsyncSession,
    event_type: str,
    aggregate_type: str,
    aggregate_id: str,
    payload: Dict[str, Any]
) -> EventOutbox:
    """Enqueue an event in outbox table."""
    event = EventOutbox(
        event_type=event_type,
        aggregate_type=aggregate_type,
        aggregate_id=aggregate_id,
        payload_json=json.dumps(payload),
        status="pending"
    )
    db.add(event)
    await db.commit()
    return event

async def process_outbox_queue(db: AsyncSession, batch_size: int = 50) -> Dict[str, Any]:
    """Process pending events in outbox."""
    stmt = select(EventOutbox).where(EventOutbox.status == "pending").limit(batch_size)
    res = await db.execute(stmt)
    events = res.scalars().all()

    processed_count = 0
    now = datetime.now(timezone.utc)
    for ev in events:
        # In a real environment dispatch SMTP/OneSignal/Webhook
        ev.status = "processed"
        ev.processed_at = now
        processed_count += 1

    await db.commit()
    return {"processed": processed_count, "pending_remaining": max(0, len(events) - processed_count)}
