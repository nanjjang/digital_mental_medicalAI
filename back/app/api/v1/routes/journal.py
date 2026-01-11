from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import JournalEntry
from app.schemas import JournalCreate, JournalOut

router = APIRouter(tags=["journal"])


@router.post("/journal", response_model=JournalOut)
def create_entry(payload: JournalCreate, db: Session = Depends(get_db)):
    entry = JournalEntry(
        user_id=payload.user_id,
        content=payload.content,
        mood_tag=payload.mood_tag,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/journal", response_model=list[JournalOut])
def list_entries(user_id: int, db: Session = Depends(get_db)):
    return (
        db.query(JournalEntry)
        .filter(JournalEntry.user_id == user_id)
        .order_by(desc(JournalEntry.created_at))
        .all()
    )