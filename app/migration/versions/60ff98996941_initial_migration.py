"""Initial migration

Revision ID: 60ff98996941
Revises: d022109725e2
Create Date: 2025-01-22 16:28:46.320767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60ff98996941'
down_revision: Union[str, None] = 'd022109725e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'subscribers_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'subscribers_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
