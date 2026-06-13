from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import (
    auth,
    chat,
    checkins,
    consents,
    goals,
    health,
    history,
    journal,
    messages,
    sessions,
    settings as settings_routes,
    summaries,
    support,
    users,
)
from app.core.config import settings
from app.db.session import init_db
from app.services.inference import get_model_runner

app = FastAPI(title=settings.project_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    get_model_runner()


app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(consents.router, prefix="/api/v1")
app.include_router(checkins.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(sessions.router, prefix="/api/v1")
app.include_router(messages.router, prefix="/api/v1")
app.include_router(summaries.router, prefix="/api/v1")
app.include_router(goals.router, prefix="/api/v1")
app.include_router(journal.router, prefix="/api/v1")
app.include_router(settings_routes.router, prefix="/api/v1")
app.include_router(history.router, prefix="/api/v1")
app.include_router(support.router, prefix="/api/v1")
