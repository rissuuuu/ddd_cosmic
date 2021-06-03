import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

metadata = sa.MetaData()

batches = sa.Table(
    "batches",
    metadata,
    sa.Column("ref", postgresql.UUID(as_uuid=False), primary_key=True,unique=True),
    sa.Column("sku", sa.String(255)),
    sa.Column("eta", sa.TIMESTAMP(timezone=True),
              default=sa.func.now()
              ),
    sa.Column("purchased_qty",sa.Integer,nullable=False)
)
