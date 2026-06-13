from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import ChatSession, Message
from app.schemas import ChatRequest, ChatResponse
from app.services.inference import get_model_runner

router = APIRouter(tags=["chat"])

_REPLIES: dict[str, dict] = {
    "suicide": {
        "high": (
            "지금 말해준 내용이 매우 무겁게 느껴져요. 혼자가 아니라는 걸 꼭 기억해 주세요. "
            "가능하다면 지금 안전한 사람에게 연락하거나 전문가와 연결해 보시는 걸 권해요. "
            "한국에서는 자살예방상담전화 1393, 정신건강위기 상담 1577-0199에서 도움을 받을 수 있어요. "
            "지금 가장 힘든 부분이 무엇인지 한 가지만 더 알려줄 수 있을까요?"
        ),
        "low": (
            "지금 마음이 많이 흔들리고 있는 것 같아요. 지금 혼자 버티고 있지 않도록 가까운 사람과 연결해 보세요. "
            "괜찮다면 지금의 감정을 조금 더 구체적으로 이야기해 볼까요?"
        ),
    },
    "depression": (
        "최근 기분이 가라앉아 있을 수 있어 보여요. 하루 중 가장 무거웠던 순간이나 반복되는 생각이 있나요? "
        "작게라도 숨 쉴 수 있었던 순간을 함께 찾아볼까요?"
    ),
    "anxiety": (
        "불안이 올라오는 순간이 있었던 것 같아요. 지금 몸이나 호흡에서 느껴지는 변화가 있나요? "
        "원한다면 1분 호흡 루틴으로 함께 안정화를 시도해 볼 수 있어요."
    ),
    "normal": (
        "말해줘서 고마워요. 오늘 하루를 더 잘 이해하기 위해 이어서 이야기해 주세요. "
        "특히 감정이 크게 변한 순간이 있었다면 알려줄 수 있을까요?"
    ),
}


def _build_reply(label: str, confidence: float) -> str:
    entry = _REPLIES.get(label, _REPLIES["normal"])
    if isinstance(entry, dict):
        return entry["high"] if confidence >= 0.6 else entry["low"]
    return entry


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    message = payload.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    session = None
    if payload.session_id:
        session = db.get(ChatSession, payload.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

    if session is None:
        session = ChatSession(user_id=payload.user_id, severity_score=0)
        db.add(session)
        db.commit()
        db.refresh(session)

    db.add(Message(session_id=session.id, role="user", content=message))
    db.flush()

    result = get_model_runner().predict(message)
    confidence = max(result.scores.values()) if result.scores else 0.0
    reply = _build_reply(result.label, confidence)

    db.add(Message(
        session_id=session.id,
        role="assistant",
        content=reply,
        meta={"label": result.label, "scores": result.scores, "confidence": confidence},
    ))
    db.commit()

    return ChatResponse(
        session_id=session.id,
        reply=reply,
        label=result.label,
        scores=result.scores,
        confidence=confidence,
    )
