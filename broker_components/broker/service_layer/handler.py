from broker_components.broker.domain import model
from broker_components.broker.domain import command


async def add_broker(cmd: command.AddBroker) -> model.Broker:
    return await model.broker_factory(
        broker_id=cmd.broker_id,
        broker_name=cmd.broker_name,
        phone=cmd.phone,
        address=cmd.address,
    )


async def update_broker(cmd: command.UpdateBrokerCommand) -> model.Broker:
    if isinstance(cmd, command.UpdateBroker):
        return await cmd.broker.update(
            {
                "broker_name": cmd.broker_name,
                "phone": cmd.phone,
                "address": cmd.address,
            }
        )
