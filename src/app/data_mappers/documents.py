from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.documents import Document, Encryption


async def get_document(resource_path: str, session: AsyncSession) -> Document:
    stmt = select(Document).where(Document.resource_path == resource_path).limit(1)
    res = await session.execute(stmt)
    return res.scalar()

