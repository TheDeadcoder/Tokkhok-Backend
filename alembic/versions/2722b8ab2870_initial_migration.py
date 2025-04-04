"""Initial migration

Revision ID: 2722b8ab2870
Revises: cb38951c7700
Create Date: 2025-03-24 19:56:46.995440

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2722b8ab2870'
down_revision: Union[str, None] = 'cb38951c7700'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('friends', sa.Column('friend_id', sa.UUID(), nullable=False))
    op.create_foreign_key(None, 'friends', 'user', ['friend_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'friends', type_='foreignkey')
    op.drop_column('friends', 'friend_id')
    # ### end Alembic commands ###
