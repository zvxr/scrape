from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref

from src.scrape.models.base import Base, GUID


class Encryption(Base):
    __tablename__ = "encryption"

    description = Column(String, nullable=False)


class Keyword(Base):
    __tablename__ = "keyword"

    document_id = Column(GUID(), ForeignKey("document.id"))


class Documents(Base):
    __tablename__ = "document"

    resource_path = Column(String, nullable=False, unique=True)
    url = Column(String, nullable=False)
    encryption_id = Column(GUID(), ForeignKey("encryption.id"))
    keywords = relationship("Keyword", backref=backref("document"))
    should_update = Column(Boolean, default=False, nullable=False)
