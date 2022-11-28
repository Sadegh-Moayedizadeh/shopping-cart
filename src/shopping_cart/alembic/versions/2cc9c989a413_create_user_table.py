"""create user table

Revision ID: 2cc9c989a413
Revises: 
Create Date: 2022-11-25 19:07:45.380208

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '2cc9c989a413'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('full_name', sa.String, index=True),
        sa.Column('email', sa.String, unique=True, index=True, nullable=False),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('is_superuser', sa.Boolean(), default=False)
    )


def downgrade():
    op.drop_table('user')
