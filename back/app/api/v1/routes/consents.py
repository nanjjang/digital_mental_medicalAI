from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Consent
from app.schemas import ConsentCreate, ConsentOut

router = APIRouter(tags=["consents"])


@router.post("/consents", response_model=ConsentOut)
def create_consent(payload: ConsentCreate, db: Session = Depends(get_db)):
    consent = Consent(
        user_id=payload.user_id,
        privacy_accepted=payload.privacy_accepted,
        safety_accepted=payload.safety_accepted,
    )
    db.add(consent)
    db.commit()
    db.refresh(consent)
    return consent


@router.get("/consents/{user_id}", response_model=ConsentOut | None)
def get_latest_consent(user_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Consent)
        .filter(Consent.user_id == user_id)
        .order_by(desc(Consent.created_at))
        .first()
    )