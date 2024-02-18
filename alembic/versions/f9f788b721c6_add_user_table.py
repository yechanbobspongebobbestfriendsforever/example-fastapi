"""add user table

Revision ID: f9f788b721c6
Revises: 63c6976a94ab
Create Date: 2024-02-11 21:25:39.290376

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9f788b721c6'
down_revision: Union[str, None] = '63c6976a94ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created_at", 
                  sa.TIMESTAMP(timezone=True), 
                  server_default=sa.text('now()'), 
                  nullable=False
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
