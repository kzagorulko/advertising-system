"""companies and measures

Revision ID: 72f8d1695bdc
Revises: 0c0a88cb1f49
Create Date: 2021-03-28 20:09:38.879794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72f8d1695bdc'
down_revision = '0c0a88cb1f49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'measures',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'advertising_companies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('excepted_profit', sa.Float(), nullable=False),
        sa.Column('profit', sa.Float(), nullable=False),
        sa.Column('title', sa.String(length=50), nullable=False),
        sa.Column('measure_id', sa.Integer(), nullable=False),
        sa.Column('creator_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(tuple(['creator_id']), ['users.id'], ),
        sa.ForeignKeyConstraint(tuple(['measure_id']), ['measures.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('advertising_companies')
    op.drop_table('measures')
    # ### end Alembic commands ###
