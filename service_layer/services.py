import json

from exceptions.exceptions import InvalidSku
from domain import command, model
from service_layer import abstract, handlers, unit_of_work
from adapters import repository
from service_layer import unit_of_work


def add_batch(
        validated_data: abstract.AddBatch,
        uow: unit_of_work.FakeUnitOfWork):
    with uow() as uw:
        product = uw.products.get(sku=validated_data.sku)
        if product is None:
            product = model.Product(sku=validated_data.sku, batches=[],
                                    events=[])
            uw.products.add(product)
        batch = handlers.add_batch(command.AddBatch(
            purchased_quantity=validated_data.purchased_quantity,
            sku=validated_data.sku
        )
        )
        product.batches.append(batch)
        uw.commit()
        print("\n_____________________________________________________________Create Batch_________________________________________________________________")

        print("Batch: ",batch,"\nProduct:", product)
    return "ok"


def get_batches(
        uow=unit_of_work.FakeUnitOfWork):
    with uow() as uw:
        batches=uw.batches
        products=uw.products.list()
        uw.commit()
    print("\n_____________________________________________________________Get Data_________________________________________________________________")
    print("Batches:",batches,"\nProducts:",products)


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def allocate(
        validated_data: abstract.AddOrderLine,
        uow: unit_of_work.FakeUnitOfWork):
    order_line = handlers.add_orderline(
        command.AddOrderLine(
            sku=validated_data.sku,
            qty=validated_data.qty
        )
    )
    with uow() as uw:
        product = uw.products.get(sku=validated_data.sku)
        if product is None:
            return f"Cannot allocate  invalid sku {order_line.sku}"
        batchref = product.allocate(order_line)
        uw.commit()
        print("\n_____________________________________________________________Allocated orderline_________________________________________________________________")
        print(product)
    return str(batchref)
