"""V1.13 Update the available quantity in Instock products

Revision ID: 0901906a0ed4
Revises: 38e5fb0016e9
Create Date: 2024-09-02 15:04:17.304248

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0901906a0ed4'
down_revision: Union[str, None] = '38e5fb0016e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bike_product_association')
    op.create_foreign_key(None, 'invoice_products', 'master products', ['EPC_code'], ['EPC_code'])
    op.create_foreign_key(None, 'invoice_products', 'cities', ['city'], ['city_id'])
    op.create_foreign_key(None, 'master products', 'GST', ['gst'], ['gst_id'])
    op.create_foreign_key(None, 'master products', 'unit', ['unit'], ['unit_id'])
    op.create_foreign_key(None, 'master products', 'colors', ['color'], ['color_id'])
    op.create_foreign_key(None, 'master products', 'new_category', ['category'], ['category_id'])
    op.create_foreign_key(None, 'master products', 'size', ['size'], ['size_id'])
    op.alter_column('product_stock', 'available_quantity',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=True,
               postgresql_using="available_quantity::integer")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('product_stock', 'available_quantity',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    op.drop_constraint(None, 'master products', type_='foreignkey')
    op.drop_constraint(None, 'master products', type_='foreignkey')
    op.drop_constraint(None, 'master products', type_='foreignkey')
    op.drop_constraint(None, 'master products', type_='foreignkey')
    op.drop_constraint(None, 'master products', type_='foreignkey')
    op.drop_constraint(None, 'invoice_products', type_='foreignkey')
    op.drop_constraint(None, 'invoice_products', type_='foreignkey')
    op.create_table('bike_product_association',
    sa.Column('bike_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('product_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['bike_id'], ['bikes.bike_id'], name='bike_product_association_bike_id_fkey'),
    sa.ForeignKeyConstraint(['product_id'], ['master products.EPC_code'], name='bike_product_association_product_id_fkey'),
    sa.PrimaryKeyConstraint('bike_id', 'product_id', name='bike_product_association_pkey')
    )
    # ### end Alembic commands ###