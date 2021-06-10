import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
metadata = sa.MetaData()

company = sa.Table(
        "company",
        metadata,
        sa.Column("id",postgresql.UUID(as_uuid=False),primary_key=True),
        sa.Column("company_name",sa.String(255),unique=True),
        sa.Column("company_symbol", sa.String(255), unique=True),
        sa.Column("sector",sa.String(255)),
        sa.Column("listed_shares",sa.String(255)),
        sa.Column("paid_up_values",sa.Float()),
        sa.Column("total_paid_up_values",sa.String(255)),
        sa.Column("created_at",sa.TIMESTAMP(timezone=True),default = sa.func.now()),
        sa.Column("updated_at",sa.TIMESTAMP(timezone=True),
                  default=sa.func.now(),
                  onupdate=sa.func.now())
)