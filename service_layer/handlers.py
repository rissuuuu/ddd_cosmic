from adapters import redis_eventpublisher
from domain import commands
from domain import events
from domain import model
from service_layer import handler
from service_layer import unit_of_work


async def add_batch(
        uow: unit_of_work.FakeUnitOfWork,
        command: commands.CreateBatch
):
    with uow() as uw:
        product = await uw.products.get(sku=command.sku)
        if product is None:
            product = model.Product(sku=command.sku, batches=[],
                                    events=[])

            await uw.products.add(product)
        batch = await handler.add_batch(commands.AddBatch(
            purchased_quantity=command.qty,
            sku=command.sku
        )
        )
        uw.batches.add(batch)
        product.batches.append(batch)
        await uw.commit()
        print("\n_____________________________________________________________Create Batch_________________________________________________________________")

        print("Batch: ",batch,"\nProduct:", product)
    return str(batch.ref)


async def get_batches(
        uow=unit_of_work.FakeUnitOfWork):
    with uow() as uw:
        batches=uw.batches
        products=await uw.products.list()
        await uw.commit()
    print("\n_____________________________________________________________Get Data_________________________________________________________________")
    print("Batches:",batches,"\nProducts:",products)


async def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


async def allocate(
        command: commands.Allocate,
        uow: unit_of_work.FakeUnitOfWork):
    order_line = await handler.add_orderline(
        commands.AddOrderLine(
            sku=command.sku,
            qty=command.qty
        )
    )
    with uow() as uw:
        product = await uw.products.get(sku=command.sku)
        if product is None:
            return f"Cannot allocate  invalid sku {order_line.sku}"
        batchref = await product.allocate(order_line)
        await uw.commit()
        print("\n_____________________________________________________________Allocated orderline_________________________________________________________________")
        print(product)
    return str(batchref)

async def sendmail(email, message):
    print(
        "___________________________________________Event Triggered__________________________________________________")
    print(email, message)

async def send_out_of_stock_notification(
        event: events.OutOfStock,
        uow: unit_of_work.FakeUnitOfWork,
):
    await sendmail("rissuuuu@gmail.com","Out of stock")

async def change_batch_quantity(
        command: commands.ChangeBatchQuantity,
        uow: unit_of_work.FakeUnitOfWork,
):
    with uow() as uw:
        product = await uw.products.get_by_batchref(batchref=command.ref)
        await product.change_batch_quantity(ref=command.ref, qty=command.qty)
        await uw.commit()
        print("\n_____________________________________________________________Change batch qty_________________________________________________________________")
        print(await uw.products.list())
    return "ok"


async def publish_allocated_event(
        event: events.Allocated,
        uow: unit_of_work.FakeUnitOfWork,
):
    print("\n____________________event captured in handler________________________\n", event)
    await redis_eventpublisher.publish("line_allocated", event)


async def publish_batch_quantity_changed(
        event: events.BatchQuantityChanged,
        uow: unit_of_work.FakeUnitOfWork,
):
    print("\n____________________event captured in handler________________________\n", event)
    await redis_eventpublisher.publish("change_batch_quantity", event)
