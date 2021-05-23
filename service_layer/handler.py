from service_layer import abstract
from domain import command
from domain.model import BatchFactory,Batch, OrderLine, OrderLineFactory

def add_batch(cmd:command.AddBatch) -> Batch:
    return BatchFactory(
        purchased_quantity = cmd.purchased_quantity,
        sku = cmd.sku
    )


def add_orderline(cmd:command.AddOrderLine) -> OrderLine:
    return OrderLineFactory(
        sku = cmd.sku,
        qty = cmd.qty
    )