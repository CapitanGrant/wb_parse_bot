"""add subscribers_id

Revision ID: d022109725e2
Revises: ccf0a108c281
Create Date: 2025-01-22 16:00:22.526739

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd022109725e2'
down_revision: Union[str, None] = 'ccf0a108c281'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('subscribers_id', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'products', ['subscribers_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'products', type_='unique')
    op.drop_column('products', 'subscribers_id')
    # ### end Alembic commands ###
