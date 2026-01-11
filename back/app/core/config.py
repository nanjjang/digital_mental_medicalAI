from __future__ import annotations

import os


class Settings:
    def __init__(self) -> None:
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./app.db")
        self.project_name = os.getenv("PROJECT_NAME", "digital_mental_medicalAI")


settings = Settings()