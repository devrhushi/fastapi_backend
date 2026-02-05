"""add foreign key and columns to post table

Revision ID: 6527e1ee2c64
Revises: a54be73bfaf0
Create Date: 2026-02-04 18:11:16.370271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6527e1ee2c64'
down_revision: Union[str, Sequence[str], None] = 'a54be73bfaf0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Adding the remaining columns from your Posts model
    """Upgrade schema."""
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_default='True', nullable=False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                                     server_default=sa.text('now()'), nullable=False))
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    
    # Adding the Foreign Key constraint and linking it to the users table
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", 
                          local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    """Downgrade schema."""
    # Dropping the constraint first, then the columns
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'content')




