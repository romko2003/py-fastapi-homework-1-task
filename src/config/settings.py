from __future__ import annotations
from functools import lru_cache
from pydantic import BaseSettings
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
DB_PATH = SRC_DIR / "database" / "source" / "movies.db"
TEST_DB_PATH = SRC_DIR / "database" / "source" / "test_movies.db"


class Settings(BaseSettings):
    TESTING: bool = False
    DB_URL: str = f"sqlite+aiosqlite:///{DB_PATH}"
    TEST_DB_URL: str = f"sqlite+aiosqlite:///{TEST_DB_PATH}"

    class Config:
        env_prefix = ""  # можна підхоплювати з ENV, якщо треба


@lru_cache
def get_settings() -> Settings:
    return Settings()
