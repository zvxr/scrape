from uuid import UUID

import aiofiles

from src.app.crypto import decrypt
from src.app.db import db_session
from src.app.models.documents import Document, EncryptionEnum
from src.app.data_mappers.documents import get_document, get_encryption


class Reader:
    def __init__(self, data: bytes):
        self.data = data

    @classmethod
    async def from_document(cls, document: Document, encryption: EncryptionEnum):
        async with aiofiles.open(document.file_path, mode="rb") as fl:
            encrypted = await fl.read()
        decrypted = decrypt(encrypted, encryption.enum_id)
        return cls(data=decrypted)

    @classmethod
    async def from_document_id(cls, document_id: UUID):
        async with db_session() as session:
            encryption = await get_encryption(EncryptionEnum.fernet.name, session)
            document = await get_document(document_id, session)
            return await cls.from_document(document, encryption)
