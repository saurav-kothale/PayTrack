"""V1.5 change Gst number in vendor

Revision ID: bc58225e3527
Revises: be3570ff3c66
Create Date: 2024-08-27 12:34:01.426895

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc58225e3527'
down_revision: Union[str, None] = 'be3570ff3c66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'master products', ['EPC_code'])
    op.alter_column('vendor_category', 'Vendor_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('vendor_category', 'GST_Number',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)
    op.drop_column('vendor_category', 'vendor_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vendor_category', sa.Column('vendor_id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.alter_column('vendor_category', 'GST_Number',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('vendor_category', 'Vendor_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint(None, 'master products', type_='unique')
    # ### end Alembic commands ###
