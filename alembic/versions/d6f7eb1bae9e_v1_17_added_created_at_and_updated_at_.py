"""V1.17 Added created at and updated at in used product

Revision ID: d6f7eb1bae9e
Revises: 26e00124e0e0
Create Date: 2024-09-16 16:20:09.509193

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6f7eb1bae9e'
down_revision: Union[str, None] = '26e00124e0e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('used products', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('used products', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.create_foreign_key(None, 'used products', 'master products', ['EPC_code'], ['EPC_code'])
    op.create_foreign_key(None, 'used products', 'cities', ['city'], ['city_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'used products', type_='foreignkey')
    op.drop_constraint(None, 'used products', type_='foreignkey')
    op.drop_column('used products', 'updated_at')
    op.drop_column('used products', 'created_at')
    # ### end Alembic commands ###
