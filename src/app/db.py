from contextlib import asynccontextmanager

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.app.settings import get_settings


@asynccontextmanager
async def db_session():
    settings = get_settings()
    engine = create_async_engine(f"sqlite+aiosqlite:///{settings.db_file}")
    async with AsyncSession(engine) as session:
        async with session.begin():
            yield session
        await session.commit()
    await engine.dispose()
