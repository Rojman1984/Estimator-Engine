"""Application configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    """Environment-backed settings for the estimator API."""

    app_name: str
    app_version: str
    monday_api_token: str | None
    monday_board_id: int | None


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings instance."""

    board_id_raw = os.getenv("MONDAY_BOARD_ID")
    board_id = int(board_id_raw) if board_id_raw else None
    return Settings(
        app_name=os.getenv("APP_NAME", "Estimator Engine API"),
        app_version=os.getenv("APP_VERSION", "0.1.0"),
        monday_api_token=os.getenv("MONDAY_API_TOKEN"),
        monday_board_id=board_id,
    )
