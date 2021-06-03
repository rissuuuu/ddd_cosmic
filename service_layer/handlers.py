from typing import Callable

from domain import commands
from domain import events
from domain import model
from service_layer import handler
from service_layer import unit_of_work


##handler only returns domain model

async def add_batch(
        command: commands.CreateBatch,
        uow: unit_of_work.AbstractUnitOfWork,

):
    with uow :
        product = await uow.products.get(sku=command.sku)
        if product is None:
            product = model.Product(sku=command.sku, batches=[],
                                    events=[])

            await uow.products.add(product)
        batch = await handler.add_batch(commands.AddBatch(
            purchased_quantity=command.qty,
            sku=command.sku
        )
        )
        await uow.batches.add(batch)
        product.batches.append(batch)
        await uow.commit()
        print("\n_____________________________________________________________Create Batch_________________________________________________________________")

        print("Batch: ",batch,"\nProduct:", product)
    return str(batch.ref)


async def get_batches(
        uow:unit_of_work.AbstractUnitOfWork):
    with uow:
        batches=uow.batches
        products=await uow.products.list()
        await uow.commit()
    print("\n_____________________________________________________________Get Data_________________________________________________________________")
    print("Batches:",batches,"\nProducts:",products)


async def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


async def allocate(
        command: commands.Allocate,
        uow: unit_of_work.AbstractUnitOfWork):
    order_line = await handler.add_orderline(
        commands.AddOrderLine(
            sku=command.sku,
            qty=command.qty
        )
    )
    with uow:
        product = await uow.products.get(sku=command.sku)
        if product is None:
            return f"Cannot allocate  invalid sku {order_line.sku}"
        batchref = await product.allocate(order_line)
        await uow.commit()
        print("\n_____________________________________________________________Allocated orderline_________________________________________________________________")
        print(product)
    return str(batchref)

async def sendmail(email, message):
    print(
        "___________________________________________Event Triggered__________________________________________________")
    print(email, message)

async def send_out_of_stock_notification(
        event: events.OutOfStock,
        publish: Callable,
):
    await sendmail("rissuuuu@gmail.com","Out of stock")

async def change_batch_quantity(
        command: commands.ChangeBatchQuantity,
        uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        product = await uow.products.get_by_batchref(batchref=command.ref)
        await product.change_batch_quantity(ref=command.ref, qty=command.qty)
        await uow.commit()
        print("\n_____________________________________________________________Change batch qty_________________________________________________________________")
        print(await uow.products.list())
    return "ok"


async def publish_allocated_event(
        event: events.Allocated,
        publish: Callable,
):
    print("\n____________________event captured in handler________________________\n", event)
    await publish("line_allocated", event)


async def publish_batch_quantity_changed(
        event: events.BatchQuantityChanged,
        publish: Callable,
):
    print("\n____________________event captured in handler________________________\n", event)
    await publish("change_batch_quantity", event)

async def add_allocation_to_read_model(
    event: events.Allocated,
    uow: unit_of_work.AbstractUnitOfWork,
):
    print("Allocated")

async def add_batch_qty_changed_to_read_model(
    event: events.BatchQuantityChanged,
    uow: unit_of_work.AbstractUnitOfWork,
):
    print("Batch Quantity Changed")

EVENT_HANDLERS = {
    events.Allocated: [publish_allocated_event,add_allocation_to_read_model],
    events.BatchQuantityChanged: [publish_batch_quantity_changed,add_batch_qty_changed_to_read_model],
    events.OutOfStock: [send_out_of_stock_notification],
}

COMMAND_HANDLERS = {
    commands.Allocate: allocate,
    commands.CreateBatch: add_batch,
    commands.ChangeBatchQuantity: change_batch_quantity,
}