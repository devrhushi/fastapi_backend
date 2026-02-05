"""add content column for post table

Revision ID: ad54d4ba2e72
Revises: 5e7d829bb759
Create Date: 2026-02-04 17:51:55.153022

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad54d4ba2e72'
down_revision: Union[str, Sequence[str], None] = '5e7d829bb759'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
