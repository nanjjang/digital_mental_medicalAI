from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import CheckIn
from app.schemas import CheckInCreate, CheckInOut
from app.services import compute_severity

router = APIRouter(tags=["checkins"])


@router.post("/checkins", response_model=CheckInOut)
def create_checkin(payload: CheckInCreate, db: Session = Depends(get_db)):
    severity = payload.severity_score
    if severity is None:
        severity = compute_severity(
            [payload.mood, payload.anxiety, payload.sleep_quality, payload.energy, payload.support]
        )
    checkin = CheckIn(
        user_id=payload.user_id,
        mood=payload.mood,
        anxiety=payload.anxiety,
        sleep_quality=payload.sleep_quality,
        energy=payload.energy,
        support=payload.support,
        severity_score=severity,
    )
    db.add(checkin)
    db.commit()
    db.refresh(checkin)
    return checkin


@router.get("/checkins", response_model=list[CheckInOut])
def list_checkins(user_id: int, db: Session = Depends(get_db)):
    return (
        db.query(CheckIn)
        .filter(CheckIn.user_id == user_id)
        .order_by(desc(CheckIn.created_at))
        .all()
    )