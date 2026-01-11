from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import CheckIn
from app.schemas import CheckInOut

router = APIRouter(tags=["history"])


@router.get("/history", response_model=list[CheckInOut])
def history(user_id: int, db: Session = Depends(get_db)):
    return (
        db.query(CheckIn)
        .filter(CheckIn.user_id == user_id)
        .order_by(desc(CheckIn.created_at))
        .limit(30)
        .all()
    )