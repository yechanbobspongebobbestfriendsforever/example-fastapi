"""add content column to posts table

Revision ID: 63c6976a94ab
Revises: 40a6497bcb09
Create Date: 2024-02-11 21:10:28.940983

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63c6976a94ab'
down_revision: Union[str, None] = '40a6497bcb09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts", 
        sa.Column(
            "content",
            sa.String(), 
            nullable=False
        )
    )
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
