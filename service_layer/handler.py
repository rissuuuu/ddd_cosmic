from service_layer import abstract
from domain import commands
from domain.model import BatchFactory,Batch, OrderLine, OrderLineFactory

def add_batch(cmd:commands.AddBatch) -> Batch:
    return BatchFactory(
        purchased_quantity = cmd.purchased_quantity,
        sku = cmd.sku
    )


def add_orderline(cmd:commands.AddOrderLine) -> OrderLine:
    return OrderLineFactory(
        sku = cmd.sku,
        qty = cmd.qty
    )