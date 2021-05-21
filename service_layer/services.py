import json

from exceptions.exceptions import InvalidSku
from domain import command,model
from service_layer import abstract,handlers, unit_of_work
from adapters import repository
from service_layer import unit_of_work


def add_batch(
    validated_data:abstract.AddBatch,
    uow: unit_of_work.FakeUnitOfWork):
    with uow() as uw:
        batch=handlers.add_batch(command.AddBatch(
            purchased_quantity = validated_data.purchased_quantity,
            sku =validated_data.sku
            )    
        )
        uw.batches.add(batch)
        uw.commit()
    return batch.json()

def get_batches(
    uow=unit_of_work.FakeUnitOfWork):
    with uow() as uw:
        data={}
        for batch in uw.batches:
            temp={}
            temp["ref"]=str(batch.ref)
            temp["sku"]=batch.sku
            temp["eta"]=str(batch.eta)
            temp["purchased_quantity"]=batch.purchased_quantity
            temp["available"]=batch.available_quantity
            for lines in batch.allocations:
                temp[str(lines.orderid)]=json.loads(lines.json())
            data[str(batch.ref)]=temp
        uw.commit()
    return data

def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}

def allocate(
    validated_data: abstract.AddOrderLine,
    uow:unit_of_work.AbstractUnitOfWork):

    order_line=handlers.add_orderline(
        command.AddOrderLine(
            sku = validated_data.sku,
            qty = validated_data.qty
        )
    )
    with uow() as uw:
        batches=uw.batches
        if not is_valid_sku(order_line.sku, batches): 
            return f"Cannot allocate  invalid {order_line.sku}"
        batchref = model.allocate(order_line, batches)
        uw.commit()
    return str(batchref)