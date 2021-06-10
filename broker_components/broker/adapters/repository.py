from uuid import UUID
from lib.repository import Repository, SqlAlchemyRepository
from lib.repository import DbConnection
from broker_components.broker.domain import model
from broker_components.broker.adapters.orm import broker


class Broker(Repository):
    async def add(self, model):
        return await super().add(model)

    async def get(self, ref):
        return await super().get(ref)


class SqlBrokerRepository(SqlAlchemyRepository):
    def __init__(self, db: DbConnection):
        self.db = db

    async def add(self, model: model.Broker):
        await self.db.execute(
            query=broker.insert(),
            values={
                "id": str(model.id_),
                "broker_id": model.broker_id,
                "broker_name": model.broker_name,
                "phone": model.phone,
                "address": model.address,
                "broker_id": model.broker_id,
            },
        )

    async def get(self, ref: int):
        return await self.db.fetch_one(
            query=broker.select().where(broker.c.broker_id == ref),
        )

    async def get_all_brokers(self):
        return await self.db.fetch_all(query=broker.select())

    async def update(self, model: model.Broker):
        await self.db.execute(
            query=broker.update().where(broker.c.broker_id == model.broker_id),
            values={
                "broker_name": model.broker_name,
                "phone": model.phone,
                "address": model.address,
            },
        )
