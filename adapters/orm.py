from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    MetaData

)

batches = Table(
    "batches",
    MetaData,
    Column()

)