"""
Application Configuration
"""

from functools import lru_cache
import json
import os
from typing import List

from pydantic import BaseModel, Field


def _parse_list_env(name: str, default: list[str]) -> list[str]:
    raw_value = os.getenv(name)
    if not raw_value:
        return default

    try:
        parsed = json.loads(raw_value)
        if isinstance(parsed, list):
            return [str(item) for item in parsed]
    except json.JSONDecodeError:
        pass

    return [item.strip() for item in raw_value.split(",") if item.strip()]


class Settings(BaseModel):
    """Application settings loaded from environment variables"""

    APP_NAME: str = "Nexus SENTINEL"
    API_TITLE: str = "Nexus SENTINEL API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    DATABASE_URL: str = (
        "postgresql+asyncpg://nexus_admin:sentinel_secure_2024@localhost:5432/nexus_sentinel"
    )
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_POOL_RECYCLE: int = 3600

    CORS_ORIGINS: List[str] = Field(default_factory=lambda: ["*"])
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = Field(default_factory=lambda: ["*"])
    CORS_ALLOW_HEADERS: List[str] = Field(default_factory=lambda: ["*"])


@lru_cache()
def get_settings() -> Settings:
    return Settings(
        APP_NAME=os.getenv("APP_NAME", "Nexus SENTINEL"),
        API_TITLE=os.getenv("API_TITLE", "Nexus SENTINEL API"),
        API_VERSION=os.getenv("API_VERSION", "1.0.0"),
        DEBUG=os.getenv("DEBUG", "false").lower() == "true",
        ENVIRONMENT=os.getenv("ENVIRONMENT", "development"),
        DATABASE_URL=os.getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://nexus_admin:sentinel_secure_2024@localhost:5432/nexus_sentinel",
        ),
        DATABASE_ECHO=os.getenv("DATABASE_ECHO", "false").lower() == "true",
        DATABASE_POOL_SIZE=int(os.getenv("DATABASE_POOL_SIZE", "20")),
        DATABASE_MAX_OVERFLOW=int(os.getenv("DATABASE_MAX_OVERFLOW", "20")),
        DATABASE_POOL_RECYCLE=int(os.getenv("DATABASE_POOL_RECYCLE", "3600")),
        CORS_ORIGINS=_parse_list_env("CORS_ORIGINS", ["*"]),
        CORS_ALLOW_CREDENTIALS=os.getenv(
            "CORS_ALLOW_CREDENTIALS", "true"
        ).lower()
        == "true",
        CORS_ALLOW_METHODS=_parse_list_env("CORS_ALLOW_METHODS", ["*"]),
        CORS_ALLOW_HEADERS=_parse_list_env("CORS_ALLOW_HEADERS", ["*"]),
    )
