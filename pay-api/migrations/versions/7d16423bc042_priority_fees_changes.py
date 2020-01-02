"""priority_fees_changes

Revision ID: 7d16423bc042
Revises: 00467a306afd
Create Date: 2019-12-23 10:55:10.959439

"""
from alembic import op
import sqlalchemy as sa
from datetime import date

from alembic import op
from sqlalchemy import Date, Integer, String, Float
from sqlalchemy.sql import column, table
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7d16423bc042'
down_revision = '00467a306afd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('corp_type', sa.Column('transaction_fee_code', sa.String(length=10), nullable=True))
    op.create_foreign_key(None, 'corp_type', 'fee_code', ['transaction_fee_code'], ['code'])
    op.add_column('invoice', sa.Column('transaction_fees', sa.Float(), nullable=True))
    op.drop_column('payment_line_item', 'service_fees')
    op.drop_column('payment_line_item', 'processing_fees')

    op.add_column('payment_line_item', sa.Column('future_effective_fees', sa.Float(), nullable=True))
    op.add_column('payment_line_item', sa.Column('priority_fees', sa.Float(), nullable=True))


    #Insert transaction fee code to fee_code
    fee_code_table = table("fee_code", column("code", String), column("amount", Float))
    # Fee Codes
    op.bulk_insert(
        fee_code_table, [
            {"code": "TRF01", "amount": 1.50}
        ]
    )

    # Insert transaction fee to corp type table - May need to change later
    op.execute("update corp_type set transaction_fee_code='TRF01' where code in ('BC', 'CP')")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('payment_line_item', 'priority_fees')
    op.drop_column('payment_line_item', 'future_effective_fees')
    
    op.add_column('payment_line_item', sa.Column('processing_fees', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('payment_line_item', sa.Column('service_fees', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.drop_column('invoice', 'transaction_fees')
    op.drop_constraint(None, 'corp_type', type_='foreignkey')
    op.drop_column('corp_type', 'transaction_fee_code')
    # ### end Alembic commands ###



