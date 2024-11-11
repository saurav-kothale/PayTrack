"""V1.4 Added new tables

Revision ID: be3570ff3c66
Revises: c0e5506b6729
Create Date: 2024-08-26 16:33:24.456334

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'be3570ff3c66'
down_revision: Union[str, None] = 'c0e5506b6729'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invoice details',
    sa.Column('invoice_id', sa.String(), nullable=False),
    sa.Column('invoice_number', sa.String(), nullable=True),
    sa.Column('invoice_amount', sa.Float(), nullable=True),
    sa.Column('invoice_date', sa.Date(), nullable=True),
    sa.Column('inventory_paydate', sa.Date(), nullable=True),
    sa.Column('vendor', sa.String(), nullable=True),
    sa.Column('invoice_image_id', sa.String(), nullable=True),
    sa.Column('user', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('invoice_id')
    )
    op.create_table('master products',
    sa.Column('EPC_code', sa.String(), nullable=False),
    sa.Column('product_name', sa.String(), nullable=True),
    sa.Column('HSN_code', sa.String(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('bike_category', sa.JSON(), nullable=True),
    sa.Column('size', sa.String(), nullable=True),
    sa.Column('color', sa.String(), nullable=True),
    sa.Column('unit', sa.String(), nullable=True),
    sa.Column('gst', sa.String(), nullable=True),
    sa.Column('vendor', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('user', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('EPC_code'),
    sa.UniqueConstraint('EPC_code')
    )
    op.create_table('product_usage',
    sa.Column('product_out_id', sa.String(), nullable=False),
    sa.Column('HSN_code', sa.String(), nullable=True),
    sa.Column('product_name', sa.String(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('bike_category', sa.String(), nullable=True),
    sa.Column('size', sa.String(), nullable=True),
    sa.Column('quntity', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('color', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('user', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('product_out_id')
    )
    op.create_table('products',
    sa.Column('product_id', sa.String(), nullable=False),
    sa.Column('EPC_code', sa.String(), nullable=True),
    sa.Column('product_name', sa.String(), nullable=True),
    sa.Column('HSN_code', sa.String(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('bike_category', sa.JSON(), nullable=True),
    sa.Column('size', sa.String(), nullable=True),
    sa.Column('color', sa.String(), nullable=True),
    sa.Column('unit', sa.String(), nullable=True),
    sa.Column('gst', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('user', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('product_id'),
    sa.UniqueConstraint('EPC_code')
    )
    op.create_table('invoice_products',
    sa.Column('product_id', sa.String(), nullable=False),
    sa.Column('EPC_code', sa.String(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('user', sa.JSON(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('total_amount', sa.Float(), nullable=True),
    sa.Column('amount_with_gst', sa.Float(), nullable=True),
    sa.Column('invoice_id', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['invoice_id'], ['invoice details.invoice_id'], ),
    sa.PrimaryKeyConstraint('product_id')
    )
    op.drop_table('product category')
    op.drop_table('inventory out')
    op.add_column('product_trasfer', sa.Column('from_city', sa.String(), nullable=True))
    op.add_column('product_trasfer', sa.Column('to_city', sa.String(), nullable=True))
    op.add_column('product_trasfer', sa.Column('quantity', sa.Integer(), nullable=True))
    op.drop_column('product_trasfer', 'product_name')
    op.drop_column('product_trasfer', 'quntity')
    op.drop_column('product_trasfer', 'bike_category')
    op.drop_column('product_trasfer', 'size')
    op.drop_column('product_trasfer', 'HSN_code')
    op.drop_column('product_trasfer', 'city')
    op.drop_column('product_trasfer', 'category')
    op.drop_column('product_trasfer', 'color')
    op.add_column('vendor_category', sa.Column('Vendor_id', sa.String(), nullable=True))
    op.add_column('vendor_category', sa.Column('Vendor_name', sa.String(), nullable=True))
    op.add_column('vendor_category', sa.Column('Contact_number', sa.String(), nullable=True))
    op.add_column('vendor_category', sa.Column('Address', sa.String(), nullable=True))
    op.add_column('vendor_category', sa.Column('Email_id', sa.String(), nullable=True))
    op.add_column('vendor_category', sa.Column('City', sa.String(), nullable=True))
    op.add_column('vendor_category', sa.Column('Payment_term', sa.String(), nullable=True))
    op.add_column('vendor_category', sa.Column('GST_Number', sa.Integer(), nullable=True))
    op.drop_constraint('vendor_category_vendor_name_key', 'vendor_category', type_='unique')
    op.create_unique_constraint(None, 'vendor_category', ['Vendor_id'])
    op.create_unique_constraint(None, 'vendor_category', ['Vendor_name'])
    op.drop_column('vendor_category', 'vendor_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vendor_category', sa.Column('vendor_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'vendor_category', type_='unique')
    op.drop_constraint(None, 'vendor_category', type_='unique')
    op.create_unique_constraint('vendor_category_vendor_name_key', 'vendor_category', ['vendor_name'])
    op.drop_column('vendor_category', 'GST_Number')
    op.drop_column('vendor_category', 'Payment_term')
    op.drop_column('vendor_category', 'City')
    op.drop_column('vendor_category', 'Email_id')
    op.drop_column('vendor_category', 'Address')
    op.drop_column('vendor_category', 'Contact_number')
    op.drop_column('vendor_category', 'Vendor_name')
    op.drop_column('vendor_category', 'Vendor_id')
    op.add_column('product_trasfer', sa.Column('color', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('product_trasfer', sa.Column('category', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('product_trasfer', sa.Column('city', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('product_trasfer', sa.Column('HSN_code', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('product_trasfer', sa.Column('size', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('product_trasfer', sa.Column('bike_category', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('product_trasfer', sa.Column('quntity', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('product_trasfer', sa.Column('product_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('product_trasfer', 'quantity')
    op.drop_column('product_trasfer', 'to_city')
    op.drop_column('product_trasfer', 'from_city')
    op.create_table('inventory out',
    sa.Column('product_out_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('category', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('bike_category', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('size', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('color', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('city', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('product_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('quntity', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('HSN_code', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('user', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('product_out_id', name='inventory out_pkey')
    )
    op.create_table('product category',
    sa.Column('product_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('product_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('HSN_code', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('category', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('user', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('bike_category', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('size', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('color', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('unit', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('gst', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('EPC_code', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('product_id', name='product category_pkey'),
    sa.UniqueConstraint('EPC_code', name='product category_EPC_code_key')
    )
    op.drop_table('invoice_products')
    op.drop_table('products')
    op.drop_table('product_usage')
    op.drop_table('master products')
    op.drop_table('invoice details')
    # ### end Alembic commands ###