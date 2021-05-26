from service_layer import abstract
from domain import commands
from domain.model import BatchFactory,Batch, OrderLine, OrderLineFactory

async def add_batch(cmd:commands.AddBatch) -> Batch:
    return await BatchFactory(
        purchased_quantity = cmd.purchased_quantity,
        sku = cmd.sku
    )


async def add_orderline(cmd:commands.AddOrderLine) -> OrderLine:
    return await OrderLineFactory(
        sku = cmd.sku,
        qty = cmd.qty
    )