from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import UserSettings
from app.schemas import SettingsCreate, SettingsOut

router = APIRouter(tags=["settings"])


@router.post("/settings", response_model=SettingsOut)
def upsert_settings(payload: SettingsCreate, db: Session = Depends(get_db)):
    settings = db.query(UserSettings).filter(UserSettings.user_id == payload.user_id).first()
    if settings:
        settings.tone = payload.tone
        settings.notifications_enabled = payload.notifications_enabled
        settings.guardian_contact = payload.guardian_contact
    else:
        settings = UserSettings(
            user_id=payload.user_id,
            tone=payload.tone,
            notifications_enabled=payload.notifications_enabled,
            guardian_contact=payload.guardian_contact,
        )
        db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings


@router.get("/settings/{user_id}", response_model=SettingsOut | None)
def get_settings(user_id: int, db: Session = Depends(get_db)):
    return db.query(UserSettings).filter(UserSettings.user_id == user_id).first()