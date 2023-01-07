import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.types import TypeDecorator, CHAR


# Source: https://gist.github.com/gmolveau/7caeeefe637679005a7bb9ae1b5e421e

class GUID(TypeDecorator):
    """
    Platform-independent GUID type. Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        elif not isinstance(value, uuid.UUID):
            return f"{uuid.UUID(value).int:32x}"
        else:
            return f"{value.int:32x}"

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        elif not isinstance(value, uuid.UUID):
            return uuid.UUID(value)
        else:
            return value


@as_declarative()
class Base:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = sa.Column(
        GUID(),
        primary_key=True,
        server_default=sa.text("uuid()"),
    )
    created_at = sa.Column(
        sa.DateTime,
        nullable=False,
        server_default=sa.func.now(),
    )
    updated_at = sa.Column(
        sa.DateTime,
        server_default=sa.func.now(),
        server_onupdate=sa.func.now(),
    )
