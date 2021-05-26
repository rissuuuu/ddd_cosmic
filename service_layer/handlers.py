from adapters import redis_eventpublisher
from domain import commands
from domain import events
from domain import model
from service_layer import handler
from service_layer import unit_of_work


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
        uw.batches.add(batch)
        product.batches.append(batch)
        uw.commit()
        print("\n_____________________________________________________________Create Batch_________________________________________________________________")

        print("Batch: ",batch,"\nProduct:", product)
    return str(batch.ref)


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
        product = uw.products.get_by_batchref(batchref=command.ref)
        product.change_batch_quantity(ref=command.ref, qty=command.qty)
        uw.commit()
        print("\n_____________________________________________________________Change batch qty_________________________________________________________________")
        print(uw.products.list())
    return "ok"


def publish_allocated_event(
        event: events.Allocated,
        uow: unit_of_work.FakeUnitOfWork,
):
    print("\n____________________event captured in handler________________________\n", event)
    redis_eventpublisher.publish("line_allocated", event)


def publish_batch_quantity_changed(
        event: events.BatchQuantityChanged,
        uow: unit_of_work.FakeUnitOfWork,
):
    print("\n____________________event captured in handler________________________\n", event)
    redis_eventpublisher.publish("change_batch_quantity", event)

def publish_create_batch(
        event: events.BatchCreated,
        uow: unit_of_work.FakeUnitOfWork,
):
    print("\n____________________event captured in handler________________________\n", event)
    redis_eventpublisher.publish("create_batch", event)

def publish_allocation_required(
        event: events.AllocationRequired,
        uow: unit_of_work.FakeUnitOfWork,
):
    print("\n____________________event captured in handler________________________\n", event)
    redis_eventpublisher.publish("allocation_required", event)