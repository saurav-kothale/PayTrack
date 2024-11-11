"""V1.1 New revision

Revision ID: 3ca0fadff24b
Revises: 
Create Date: 2024-08-20 17:35:17.786079

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ca0fadff24b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Use the USING clause to convert the VARCHAR column to JSON
    op.execute(
        """
        ALTER TABLE "product category" 
        ALTER COLUMN bike_category 
        TYPE JSON 
        USING bike_category::json
        """
    )


def downgrade() -> None:
    # Reverse the operation, converting JSON back to VARCHAR
    op.execute(
        """
        ALTER TABLE "product category" 
        ALTER COLUMN bike_category 
        TYPE VARCHAR 
        USING bike_category::text
        """
    )