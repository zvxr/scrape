import enum

from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref

from src.app.models.base import Base, GUID


class EncryptionEnum(enum.Enum):
    fernet = 1


class Encryption(Base):
    __tablename__ = "encryption"
    __table_args__ = {"extend_existing": True}

    enum_id = Column(Enum(EncryptionEnum), nullable=False, unique=True)
    description = Column(String, nullable=False)


class Keyword(Base):
    __tablename__ = "keyword"
    __table_args__ = {"extend_existing": True}

    document_id = Column(GUID(), ForeignKey("document.id"))


class Document(Base):
    __tablename__ = "document"
    __table_args__ = {"extend_existing": True}

    resource_path = Column(String, nullable=False, unique=True)
    url = Column(String, nullable=False)
    encryption_id = Column(GUID(), ForeignKey("encryption.id"), nullable=False)
