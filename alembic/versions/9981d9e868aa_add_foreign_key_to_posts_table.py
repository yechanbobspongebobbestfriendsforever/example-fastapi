"""add foreign-key to posts table

Revision ID: 9981d9e868aa
Revises: f9f788b721c6
Create Date: 2024-02-11 21:34:16.318520

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9981d9e868aa'
down_revision: Union[str, None] = 'f9f788b721c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        constraint_name='post_users_fk', 
        source_table='posts',
        referent_table='users', 
        local_cols=['owner_id',],
        remote_cols=['id',],
        ondelete="CASCADE"
    )
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts','owner_id')
    pass
