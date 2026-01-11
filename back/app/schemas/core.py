from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    email: str | None = None
    display_name: str = Field(default="Guest", max_length=80)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str | None
    display_name: str


class ConsentCreate(BaseModel):
    user_id: int
    privacy_accepted: bool
    safety_accepted: bool


class ConsentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    privacy_accepted: bool
    safety_accepted: bool


class CheckInCreate(BaseModel):
    user_id: int
    mood: int = Field(ge=0, le=100)
    anxiety: int = Field(ge=0, le=100)
    sleep_quality: int = Field(ge=0, le=100)
    energy: int = Field(ge=0, le=100)
    support: int = Field(ge=0, le=100)
    severity_score: int | None = Field(default=None, ge=0, le=100)


class CheckInOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    mood: int
    anxiety: int
    sleep_quality: int
    energy: int
    support: int
    severity_score: int


class ChatSessionCreate(BaseModel):
    user_id: int
    severity_score: int = Field(default=0, ge=0, le=100)


class ChatSessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    status: str
    severity_score: int


class ChatSessionUpdate(BaseModel):
    status: str | None = None
    severity_score: int | None = Field(default=None, ge=0, le=100)


class MessageCreate(BaseModel):
    session_id: int
    role: str = "client"
    content: str


class MessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: int
    role: str
    content: str


class SummaryCreate(BaseModel):
    user_id: int
    session_id: int | None = None
    summary_text: str
    risk_level: str = "low"


class SummaryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    session_id: int | None
    summary_text: str
    risk_level: str


class GoalCreate(BaseModel):
    user_id: int
    title: str
    detail: str | None = None
    status: str = "active"


class GoalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    detail: str | None
    status: str


class JournalCreate(BaseModel):
    user_id: int
    content: str
    mood_tag: str | None = None


class JournalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    content: str
    mood_tag: str | None


class SettingsCreate(BaseModel):
    user_id: int
    tone: str = "gentle"
    notifications_enabled: bool = True
    guardian_contact: str | None = None


class SettingsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    tone: str
    notifications_enabled: bool
    guardian_contact: str | None


class AuthSignup(BaseModel):
    email: EmailStr
    display_name: str = Field(default="Guest", max_length=80)
    password: str = Field(min_length=8)
    privacy_accepted: bool
    safety_accepted: bool
    terms_accepted: bool


class AuthLogin(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user: UserOut
    token: str


class SupportTicketCreate(BaseModel):
    email: EmailStr
    subject: str = Field(min_length=3, max_length=200)
    message: str = Field(min_length=5)
    user_id: int | None = None


class SupportTicketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    subject: str
    message: str
    created_at: datetime


class SupportFAQ(BaseModel):
    question: str
    answer: str


class SupportAnnouncement(BaseModel):
    title: str
    body: str
    published_at: datetime