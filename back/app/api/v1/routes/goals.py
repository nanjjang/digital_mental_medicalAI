from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Goal
from app.schemas import GoalCreate, GoalOut

router = APIRouter(tags=["goals"])


@router.post("/goals", response_model=GoalOut)
def create_goal(payload: GoalCreate, db: Session = Depends(get_db)):
    goal = Goal(
        user_id=payload.user_id,
        title=payload.title,
        detail=payload.detail,
        status=payload.status,
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


@router.get("/goals", response_model=list[GoalOut])
def list_goals(user_id: int, db: Session = Depends(get_db)):
    return db.query(Goal).filter(Goal.user_id == user_id).all()