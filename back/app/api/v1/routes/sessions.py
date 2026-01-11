from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import ChatSession
from app.schemas import ChatSessionCreate, ChatSessionOut, ChatSessionUpdate

router = APIRouter(tags=["sessions"])


@router.post("/sessions", response_model=ChatSessionOut)
def create_session(payload: ChatSessionCreate, db: Session = Depends(get_db)):
    session = ChatSession(user_id=payload.user_id, severity_score=payload.severity_score)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.patch("/sessions/{session_id}", response_model=ChatSessionOut)
def update_session(session_id: int, payload: ChatSessionUpdate, db: Session = Depends(get_db)):
    session = db.get(ChatSession, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if payload.status:
        session.status = payload.status
    if payload.severity_score is not None:
        session.severity_score = payload.severity_score
    if payload.status == "ended":
        session.ended_at = datetime.utcnow()
    db.commit()
    db.refresh(session)
    return session


@router.get("/sessions", response_model=list[ChatSessionOut])
def list_sessions(user_id: int, db: Session = Depends(get_db)):
    return (
        db.query(ChatSession)
        .filter(ChatSession.user_id == user_id)
        .order_by(desc(ChatSession.started_at))
        .all()
    )