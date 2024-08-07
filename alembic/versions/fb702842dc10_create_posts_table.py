"""create posts table

Revision ID: fb702842dc10
Revises: b46f8a96edfb
Create Date: 2024-08-04 12:33:03.320961

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision: str = 'fb702842dc10'
down_revision: Union[str, None] = 'b46f8a96edfb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', 
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('published', sa.Boolean(), nullable=False, server_default=True),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=text('now()')),
                    sa.PrimaryKeyConstraint('id'),)
    op.add_column('posts', sa.Column('user_email', sa.String(), nullable=False))
    op.create_foreign_key("post_user_fk", source_table="posts", referent_table="users", local_cols=['user_email'], remote_cols=['email'], ondelete="CASCADE")

                             
    


def downgrade() -> None:
    op.drop_table('posts')
    pass
