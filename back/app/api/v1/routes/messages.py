from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Message
from app.schemas import MessageCreate, MessageOut

router = APIRouter(tags=["messages"])


@router.post("/messages", response_model=MessageOut)
def create_message(payload: MessageCreate, db: Session = Depends(get_db)):
    message = Message(session_id=payload.session_id, role=payload.role, content=payload.content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


@router.get("/messages", response_model=list[MessageOut])
def list_messages(session_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(desc(Message.created_at))
        .all()
    )