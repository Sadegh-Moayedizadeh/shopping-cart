'''first revision

Revision ID: 6c55b5752d3a
Revises: 
Create Date: 2022-12-02 15:05:44.607882

'''
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c55b5752d3a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('full_name', sa.String(), index=True),
        sa.Column('email', sa.String(), unique=True, index=True, nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'cart',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'product',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('title', sa.String()),
        sa.Column('price', sa.Float()),
        sa.Column('category', sa.String()),
        sa.Column('description', sa.String()),
        sa.Column('image', sa.String()),
        sa.Column('cart_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('user')
    op.drop_table('cart')
    op.drop_table('product')
