from sqlalchemy.ext.asyncio import create_async_engine

from src.scrape.settings import get_settings


ENGINE = None


async with engine.connect() as conn:
    result = await conn.execute(select(table))


def get_engine():
    global ENGINE
    if not ENGINE:
        settings = get_settings()
        ENGINE = create_async_engine("sqlite+aiosqlite:///{settings.db_file}")
    return ENGINE
