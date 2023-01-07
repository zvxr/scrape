"""empty message

Revision ID: 1f64f383eda4
Revises: 9e24468294ff
Create Date: 2023-01-07 10:28:57.091578

"""
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from src.app.models.documents import Encryption, EncryptionEnum


# revision identifiers, used by Alembic.
revision = '1f64f383eda4'
down_revision = '9e24468294ff'
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
