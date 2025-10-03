from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy import text

from .models import Base
from config.settings import get_settings  # <-- ОТ ТУТ ВАЖЛИВИЙ ІМПОРТ


settings = get_settings()

# Очікуємо, що в settings є поля на кшталт:
# - DB_URL         (звичайна база, наприклад "sqlite+aiosqlite:///.../movies.db")
# - TEST_DB_URL    (для тестів; conftest зазвичай виставляє TESTING=True)
# - TESTING        (bool)
DATABASE_URL = settings.TEST_DB_URL if getattr(settings, "TESTING", False) else settings.DB_URL

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    """Створюємо таблиці, якщо їх немає (лише для SQLite/локального запуску)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # проста перевірка з’єднання
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))


async def close_db() -> None:
    """Акуратно закриваємо engine."""
    await engine.dispose()


async def get_db() -> AsyncSession:
    """DI для FastAPI: видає сесію, автоматично закриває після використання."""
    async with AsyncSessionLocal() as session:
        yield session
