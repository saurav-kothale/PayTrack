"""V1.18 added user at used product

Revision ID: 2bc895141305
Revises: d6f7eb1bae9e
Create Date: 2024-09-18 11:00:37.407907

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2bc895141305'
down_revision: Union[str, None] = 'd6f7eb1bae9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('used products', sa.Column('comment', sa.String(), nullable=True))
    op.add_column('used products', sa.Column('user', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('used products', 'user')
    op.drop_column('used products', 'comment')
    # ### end Alembic commands ###