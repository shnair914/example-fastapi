"""create user table

Revision ID: b46f8a96edfb
Revises: 
Create Date: 2024-08-04 11:16:35.770648

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql.expression import text
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b46f8a96edfb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))           
    


def downgrade() -> None:
    op.drop_table('users')
    pass
