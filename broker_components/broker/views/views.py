from broker_components.broker.adapters.orm import broker
from broker_components.broker.service_layer import unit_of_work


async def get_broker(broker_id:int,uow: unit_of_work.BrokerSqlAlchemyUnitOfWork
):
    async with uow:
        result = await uow.connection.fetch_one(
            query=broker.select().where(broker.c.broker_id == broker_id)
        )
    return result


async def get_all_brokers(uow: unit_of_work.BrokerSqlAlchemyUnitOfWork
):
    async with uow:
        result = await uow.connection.fetch_all(
            query=broker.select()
        )
    return result


