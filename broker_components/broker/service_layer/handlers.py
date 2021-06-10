from __future__ import annotations
from broker_components.broker.service_layer import abstract
from broker_components.broker.domain import command
from broker_components.broker.service_layer import unit_of_work
from broker_components.broker.service_layer import handler
from broker_components.broker.domain.model import Broker


async def add_broker(
    validated_data: abstract.AddBroker,
    uow: unit_of_work.BrokerSqlAlchemyUnitOfWork,
):
    async with uow:
        broker = await handler.add_broker(
            command.AddBroker(
                broker_id=validated_data.broker_id,
                broker_name=validated_data.broker_name,
                phone=validated_data.phone,
                address=validated_data.address,
            )
        )
        await uow.repository.add(broker)


async def update_broker(
    validated_data: abstract.UpdateProduct,
    uow: unit_of_work.BrokerSqlAlchemyUnitOfWork,
):
    async with uow:
        broker = await uow.repository.get(validated_data.broker_id)
        broker = Broker(
            id_=broker["id"],
            broker_id=broker["broker_id"],
            broker_name=broker["broker_name"],
            address=broker["address"],
            phone=broker["phone"],
        )

        cmd = command.UpdateBroker(
            broker=broker,
            broker_name=validated_data.broker_name
            if validated_data.broker_name
            else broker.broker_name,
            phone=validated_data.phone if validated_data.phone else broker.phone,
            address=validated_data.address
            if validated_data.address
            else broker.address,
        )
        broker5 = await handler.update_broker(cmd=cmd)
        await uow.repository.update(broker5)


COMMAND_HANDLERS = {
    command.AddBroker: add_broker,
    command.UpdateBroker: update_broker,
}

EVENT_HANDLERS = {}
