"""V1.19 Added bike number in used product

Revision ID: 4f893b45d805
Revises: 2bc895141305
Create Date: 2024-10-02 15:39:01.892563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f893b45d805'
down_revision: Union[str, None] = '2bc895141305'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('used products', sa.Column('bike_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('used products', 'bike_number')
    # ### end Alembic commands ###
