"""V1.10 Include city to inventory products

Revision ID: d127ab012101
Revises: 4f9d98f77736
Create Date: 2024-08-30 15:09:51.886245

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd127ab012101'
down_revision: Union[str, None] = '4f9d98f77736'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product_stock',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('EPC_code', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('available_quantity', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('invoice_products', sa.Column('city', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('invoice_products', 'city')
    op.drop_table('product_stock')
    # ### end Alembic commands ###