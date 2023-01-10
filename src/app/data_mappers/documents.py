from uuid import UUID

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.documents import Document, Encryption, EncryptionEnum


async def get_document(document_id: UUID, session: AsyncSession) -> Document:
    stmt = select(Document).where(Document.id == document_id).limit(1)
    res = await session.execute(stmt)
    return res.scalar()


async def get_document_by_resource_path(resource_path: str, session: AsyncSession) -> Document:
    stmt = select(Document).where(Document.resource_path == resource_path).limit(1)
    res = await session.execute(stmt)
    return res.scalar()


async def get_encryption(encryption: EncryptionEnum, session: AsyncSession) -> Encryption:
    stmt = select(Encryption).where(Encryption.enum_id == encryption).limit(1)
    res = await session.execute(stmt)
    return res.scalar()


async def insert_document(params: dict, session: AsyncSession) -> Document:
    stmt = insert(Document).values(**params)
    await session.execute(stmt)
