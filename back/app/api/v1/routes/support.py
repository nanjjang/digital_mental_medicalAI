from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import SupportTicket
from app.schemas import SupportAnnouncement, SupportFAQ, SupportTicketCreate, SupportTicketOut

router = APIRouter(tags=["support"])

_FAQ = [
    SupportFAQ(
        question="서비스는 의료행위를 대신하나요?",
        answer="아니요. 본 서비스는 자가 기록과 안내를 제공하며 의료행위를 대체하지 않습니다.",
    ),
    SupportFAQ(
        question="내 기록은 어떻게 보호되나요?",
        answer="암호화 저장과 최소 권한 정책을 기반으로 안전하게 관리합니다.",
    ),
]

_ANNOUNCEMENTS = [
    SupportAnnouncement(
        title="서비스 베타 오픈 안내",
        body="지속적인 개선을 위해 피드백을 받고 있습니다.",
        published_at=datetime.utcnow(),
    )
]


@router.get("/support/faq", response_model=list[SupportFAQ])
def list_faq():
    return _FAQ


@router.get("/support/announcements", response_model=list[SupportAnnouncement])
def list_announcements():
    return _ANNOUNCEMENTS


@router.post("/support/tickets", response_model=SupportTicketOut)
def create_ticket(payload: SupportTicketCreate, db: Session = Depends(get_db)):
    ticket = SupportTicket(
        user_id=payload.user_id,
        email=payload.email,
        subject=payload.subject,
        message=payload.message,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket