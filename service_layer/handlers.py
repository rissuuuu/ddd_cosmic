from domain import commands, model
from domain import events
from service_layer import abstract, handler
from service_layer import unit_of_work
from domain import  commands


def add_batch(
        uow: unit_of_work.FakeUnitOfWork,
        command: commands.CreateBatch
        ):
    with uow() as uw:
        product = uw.products.get(sku=command.sku)
        if product is None:
            product = model.Product(sku=command.sku, batches=[],
                                    events=[])
            uw.products.add(product)
        batch = handler.add_batch(commands.AddBatch(
            purchased_quantity=command.qty,
            sku=command.sku
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
        command: commands.Allocate,
        uow: unit_of_work.FakeUnitOfWork):
    order_line = handler.add_orderline(
        commands.AddOrderLine(
            sku=command.sku,
            qty=command.qty
        )
    )
    with uow() as uw:
        product = uw.products.get(sku=command.sku)
        if product is None:
            return f"Cannot allocate  invalid sku {order_line.sku}"
        batchref = product.allocate(order_line)
        uw.commit()
        print("\n_____________________________________________________________Allocated orderline_________________________________________________________________")
        print(product)
    return str(batchref)

def sendmail(email, message):
    print(
        "___________________________________________Event Triggered__________________________________________________")
    print(email, message)

def send_out_of_stock_notification(
        event: events.OutOfStock,
        uow: unit_of_work.FakeUnitOfWork,
):
    sendmail("rissuuuu@gmail.com","Out of stock")

def change_batch_quantity(
        command: commands.ChangeBatchQuantity,
        uow: unit_of_work.FakeUnitOfWork,
):
    with uow() as uw:
        product=uw.products.get_by_batchref(batchref=command.ref)
        product.change_batch_quantity(ref=command.ref,qty=command.qty)
        uw.commit()
    return "ok"
