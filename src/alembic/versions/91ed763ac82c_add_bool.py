"""add bool

Revision ID: 91ed763ac82c
Revises: 98deba041446
Create Date: 2023-01-05 11:22:37.624684

"""
from alembic import op
import sqlalchemy as sa

import src.scrape.models.base


# revision identifiers, used by Alembic.
revision = '91ed763ac82c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('keyword')
    op.drop_table('encryption')
    op.drop_table('document')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('document',
    sa.Column('id', sa.CHAR(length=32), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.Column('resource_path', sa.VARCHAR(), nullable=False),
    sa.Column('url', sa.VARCHAR(), nullable=False),
    sa.Column('encryption_id', sa.CHAR(length=32), nullable=True),
    sa.ForeignKeyConstraint(['encryption_id'], ['encryption.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('resource_path')
    )
    op.create_table('encryption',
    sa.Column('id', sa.CHAR(length=32), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.Column('description', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('keyword',
    sa.Column('id', sa.CHAR(length=32), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.Column('document_id', sa.CHAR(length=32), nullable=True),
    sa.ForeignKeyConstraint(['document_id'], ['document.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
