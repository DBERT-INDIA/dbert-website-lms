from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from pydantic import BaseModel

from backend.core.database import get_db
from backend.core.dependencies import get_current_user_token
from backend.models.features import Conversation, Message

router = APIRouter(prefix="/messages", tags=["Messaging & Alerts"])

class StartConversationRequest(BaseModel):
    counterparty_type: str
    counterparty_id: int
    initial_message: str
    post_id: Optional[int] = None

class SendMessageRequest(BaseModel):
    body: str

@router.get("", summary="List User Conversations")
async def list_conversations(
    current_user: Dict[str, Any] = Depends(get_current_user_token),
    db: AsyncSession = Depends(get_db)
):
    user_id = int(current_user.get("sub"))
    stmt = select(Conversation).where(Conversation.intern_id == user_id).order_by(Conversation.updated_at.desc())
    res = await db.execute(stmt)
    return res.scalars().all()

@router.post("/start", summary="Start New Conversation Thread")
async def start_conversation(
    req: StartConversationRequest,
    current_user: Dict[str, Any] = Depends(get_current_user_token),
    db: AsyncSession = Depends(get_db)
):
    user_id = int(current_user.get("sub"))
    conv = Conversation(
        intern_id=user_id,
        counterparty_type=req.counterparty_type,
        counterparty_id=req.counterparty_id,
        post_id=req.post_id
    )
    db.add(conv)
    await db.commit()
    await db.refresh(conv)

    msg = Message(
        conversation_id=conv.id,
        sender_type=current_user.get("role", "intern"),
        sender_id=user_id,
        body=req.initial_message
    )
    db.add(msg)
    await db.commit()

    return {"status": "success", "conversation_id": conv.id}

@router.get("/{conv_id}", summary="Get Conversation Messages")
async def get_messages(
    conv_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user_token),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Message).where(Message.conversation_id == conv_id).order_by(Message.created_at.asc())
    res = await db.execute(stmt)
    return res.scalars().all()

@router.post("/{conv_id}/send", summary="Send Message in Thread")
async def send_message(
    conv_id: int,
    req: SendMessageRequest,
    current_user: Dict[str, Any] = Depends(get_current_user_token),
    db: AsyncSession = Depends(get_db)
):
    user_id = int(current_user.get("sub"))
    msg = Message(
        conversation_id=conv_id,
        sender_type=current_user.get("role", "intern"),
        sender_id=user_id,
        body=req.body
    )
    db.add(msg)
    await db.commit()
    return {"status": "success", "message_id": msg.id}

@router.post("/{conv_id}/read", summary="Mark Messages as Read")
async def mark_read(
    conv_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user_token),
    db: AsyncSession = Depends(get_db)
):
    stmt = update(Message).where(Message.conversation_id == conv_id).values(is_read=True)
    await db.execute(stmt)
    await db.commit()
    return {"status": "success"}
