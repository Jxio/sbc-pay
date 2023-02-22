"""empty message

Revision ID: 9706d596f44b
Revises: e296910623cd
Create Date: 2023-02-21 20:11:56.836286

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9706d596f44b'
down_revision = 'e296910623cd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('invoices', sa.Column('refund_date', sa.DateTime(), nullable=True))


def downgrade():
    pass
