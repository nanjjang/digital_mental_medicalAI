from __future__ import annotations

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {},
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    if settings.database_url.startswith("sqlite"):
        _migrate_sqlite()


def _migrate_sqlite() -> None:
    migrations = [
        ("users", "phone", "VARCHAR(40)", None),
        ("users", "location", "VARCHAR(120)", None),
        ("users", "avatar_url", "VARCHAR(255)", None),
        ("users", "bio", "TEXT", None),
        ("user_settings", "daily_checkin_enabled", "BOOLEAN", "1"),
        ("user_settings", "weekly_report_enabled", "BOOLEAN", "1"),
        ("user_settings", "summary_autosave", "BOOLEAN", "0"),
        ("user_settings", "language", "VARCHAR(32)", "'ko-KR'"),
        ("user_settings", "timezone", "VARCHAR(64)", "'Asia/Seoul'"),
        ("user_settings", "data_retention_days", "INTEGER", "365"),
        ("user_settings", "marketing_opt_in", "BOOLEAN", "0"),
        ("user_settings", "crisis_alerts_enabled", "BOOLEAN", "1"),
        ("user_settings", "privacy_mode", "BOOLEAN", "0"),
    ]
    try:
        with engine.connect() as conn:
            for table, col, col_type, default in migrations:
                existing = {row[1] for row in conn.execute(text(f"PRAGMA table_info('{table}')"))}
                if col not in existing:
                    ddl = f"ALTER TABLE {table} ADD COLUMN {col} {col_type}"
                    if default is not None:
                        ddl += f" DEFAULT {default}"
                    conn.execute(text(ddl))
            conn.commit()
    except Exception:
        pass
