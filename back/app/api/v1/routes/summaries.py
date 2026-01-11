from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Summary
from app.schemas import SummaryCreate, SummaryOut

router = APIRouter(tags=["summaries"])


@router.post("/summaries", response_model=SummaryOut)
def create_summary(payload: SummaryCreate, db: Session = Depends(get_db)):
    summary = Summary(
        user_id=payload.user_id,
        session_id=payload.session_id,
        summary_text=payload.summary_text,
        risk_level=payload.risk_level,
    )
    db.add(summary)
    db.commit()
    db.refresh(summary)
    return summary


@router.get("/summaries", response_model=list[SummaryOut])
def list_summaries(user_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Summary)
        .filter(Summary.user_id == user_id)
        .order_by(desc(Summary.created_at))
        .all()
    )