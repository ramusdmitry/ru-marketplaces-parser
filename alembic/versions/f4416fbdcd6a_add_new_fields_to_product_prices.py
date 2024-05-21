"""Add new fields to product_prices

Revision ID: f4416fbdcd6a
Revises: 830bbec595d4
Create Date: 2024-05-19 18:44:06.341210

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'f4416fbdcd6a'
down_revision: Union[str, None] = '830bbec595d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_products')
    op.add_column('product_prices', sa.Column('title', sa.Text(), nullable=True))
    op.add_column('product_prices', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('product_prices', sa.Column('url', sa.Text(), nullable=True))
    op.add_column('product_prices', sa.Column('discount_percent', sa.DECIMAL(precision=5, scale=2), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product_prices', 'discount_percent')
    op.drop_column('product_prices', 'url')
    op.drop_column('product_prices', 'description')
    op.drop_column('product_prices', 'title')
    op.create_table('user_products',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('product_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', mysql.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], name='user_products_ibfk_1'),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='user_products_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###