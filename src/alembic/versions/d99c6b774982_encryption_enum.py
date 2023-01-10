"""encryption enum

Revision ID: d99c6b774982
Revises: 469b2d591a58
Create Date: 2023-01-09 15:45:54.429938

"""
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from src.app.models.documents import Encryption, EncryptionEnum


# revision identifiers, used by Alembic.
revision = 'd99c6b774982'
down_revision = '469b2d591a58'
branch_labels = None
depends_on = None


def upgrade() -> None:
    stmt = sa.insert(Encryption).values(
        id=str(uuid4()),
        enum_id=EncryptionEnum.fernet,
        description="https://cryptography.io/en/latest/fernet/"
    )
    op.execute(stmt)


def downgrade() -> None:
    pass
