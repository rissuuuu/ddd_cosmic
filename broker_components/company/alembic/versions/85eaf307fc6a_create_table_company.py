"""create table company

Revision ID: 85eaf307fc6a
Revises: 
Create Date: 2021-06-09 10:47:23.281998

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '85eaf307fc6a'
# down_revision = '930bf3414503'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "company",
        sa.Column("id", sa.VARCHAR(255)),
        sa.Column("company_name", sa.VARCHAR(255)),
        sa.Column("company_symbol",sa.VARCHAR(255)),
        sa.Column("sector", sa.VARCHAR(255)),
        sa.Column("listed_shares", sa.VARCHAR(255)),
        sa.Column("paid_up_values", sa.Float()),
        sa.Column("total_paid_up_values", sa.VARCHAR(255)),
        sa.Column("created_at", sa.TIMESTAMP()),
        sa.Column("updated_at", sa.TIMESTAMP()),
        sa.UniqueConstraint("company_name"),
        sa.UniqueConstraint("company_symbol"),
        sa.PrimaryKeyConstraint("id")
    )


def downgrade():
    op.drop_table("company")
