"""add product ids column to user table.

Revision ID: b75c2f1e0a8b
Revises: 2cc9c989a413
Create Date: 2022-11-29 16:30:40.046654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b75c2f1e0a8b'
down_revision = '2cc9c989a413'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'user',
        sa.Column(
            'product_ids', sa.ARRAY(sa.Integer), nullable=True, default=[])
    )


def downgrade():
    op.drop_column(
        'user',
        sa.Column(
            'product_ids', sa.ARRAY(sa.Integer), nullable=True, default=[])
    )
