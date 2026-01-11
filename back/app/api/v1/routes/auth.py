from __future__ import annotations

from datetime import datetime, timedelta
import secrets

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import AuthToken, Consent, User
from app.schemas import AuthLogin, AuthResponse, AuthSignup, UserOut
from app.services import hash_password, verify_password

router = APIRouter(tags=["auth"])


@router.post("/auth/signup", response_model=AuthResponse)
def signup(payload: AuthSignup, db: Session = Depends(get_db)):
    if not payload.terms_accepted:
        raise HTTPException(status_code=400, detail="Terms must be accepted")

    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=payload.email,
        display_name=payload.display_name,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    consent = Consent(
        user_id=user.id,
        privacy_accepted=payload.privacy_accepted,
        safety_accepted=payload.safety_accepted,
    )
    db.add(consent)

    token_value = secrets.token_urlsafe(32)
    token = AuthToken(
        user_id=user.id,
        token=token_value,
        expires_at=datetime.utcnow() + timedelta(days=7),
    )
    db.add(token)
    db.commit()

    return AuthResponse(user=UserOut.model_validate(user), token=token_value)


@router.post("/auth/login", response_model=AuthResponse)
def login(payload: AuthLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_value = secrets.token_urlsafe(32)
    token = AuthToken(
        user_id=user.id,
        token=token_value,
        expires_at=datetime.utcnow() + timedelta(days=7),
    )
    db.add(token)
    db.commit()

    return AuthResponse(user=UserOut.model_validate(user), token=token_value)