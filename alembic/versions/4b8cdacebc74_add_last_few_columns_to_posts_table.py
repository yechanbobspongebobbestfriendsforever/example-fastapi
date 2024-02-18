"""add last few columns to posts table

Revision ID: 4b8cdacebc74
Revises: 9981d9e868aa
Create Date: 2024-02-11 21:40:47.135361

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b8cdacebc74'
down_revision: Union[str, None] = '9981d9e868aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts", 
        sa.Column("published", 
                  sa.Boolean(), 
                  nullable=False, 
                  server_default="TRUE"
        )
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at", 
            sa.TIMESTAMP(timezone=True), 
            server_default=sa.text('NOW()'), 
            nullable=False
        )
    )

def downgrade() -> None:
    op.drop_column("posts","published")
    op.drop_column("posts","created_at")
        
    pass
