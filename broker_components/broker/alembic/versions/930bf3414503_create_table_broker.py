"""create table broker

Revision ID: 930bf3414503
Revises: 
Create Date: 2021-06-07 11:00:57.726318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '930bf3414503'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "broker",
        sa.Column("id", sa.VARCHAR(255)),
        sa.Column("broker_id", sa.Integer(), nullable=False),
        sa.Column("broker_name", sa.VARCHAR(255), nullable=False),
        sa.Column("phone", sa.VARCHAR(255), nullable=False),
        sa.Column("address", sa.VARCHAR(255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("broker_id"),
        sa.UniqueConstraint("broker_name"),
        sa.UniqueConstraint("phone"),
        sa.UniqueConstraint("address")
    )


def downgrade():
    op.drop_table("broker")
