import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.expression import null
metadata = sa.MetaData()

broker = sa.Table(
    "broker",
    metadata,
    sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
    sa.Column("broker_id", sa.Integer, unique=True, nullable=False),
    sa.Column("broker_name", sa.String(255), unique=True, nullable=False),
    sa.Column("phone", sa.String(255), unique=True, nullable=False),
    sa.Column("address", sa.String(255), nullable=False)
)
