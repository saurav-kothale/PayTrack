"""V1.15 Added relationship to instock product to city

Revision ID: 28834cee1780
Revises: 1264ab9f62a4
Create Date: 2024-09-05 15:05:00.107763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28834cee1780'
down_revision: Union[str, None] = '1264ab9f62a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'product_stock', 'cities', ['city'], ['city_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product_stock', type_='foreignkey')
    # ### end Alembic commands ###