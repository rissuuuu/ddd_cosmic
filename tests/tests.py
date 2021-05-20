from domain.model import Batch,OrderLine,allocate
import datetime
from adapters import repository

def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch(ref="batch-001", sku="SMALL-TABLE", purchased_quantity=20)
    line = OrderLine(orderid="order-ref", sku="SMALLs-TABLE", qty=2)

    batch.allocate(line)
    print(batch.allocations)
    # a=batch.allocated_quantity
    # b=batch.available_quantity
    # print(a,b)
# test_allocating_to_a_batch_reduces_the_available_quantity()

def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch(ref="in-stock-batch", sku="RETRO-CLOCK", purchased_quantity=100, eta=datetime.datetime.now())
    shipment_batch = Batch(ref="shipment-batch", sku="RETRO-CLOCK", purchased_quantity=100, eta=datetime.datetime.now()+datetime.timedelta(days=1))
    line = OrderLine(orderid="oref", sku="RETRO-CLOCK", qty=50)
    allocate(line, [in_stock_batch, shipment_batch])

    print(in_stock_batch)
    print(in_stock_batch.allocations)

test_prefers_current_stock_batches_to_shipments()
def test_repository_can_save_a_batch():
    batch1 = Batch(ref="in-stock-batch1", sku="RETRO-CLOCK", purchased_quantity=100, eta=datetime.datetime.now())
    batch2 = Batch(ref="in-stock-batch2", sku="RETRO-CLOCK", purchased_quantity=110, eta=datetime.datetime.now())
    batch3 = Batch(ref="in-stock-batch3", sku="RETRO-CLOCK", purchased_quantity=120, eta=datetime.datetime.now())
    batch4 = Batch(ref="in-stock-batch4", sku="RETRO-CLOCK", purchased_quantity=130, eta=datetime.datetime.now())

    repo = repository.FakeRepository()
    repo.add(batch1)
    repo.add(batch2)
    repo.add(batch3)
    repo.add(batch4)
    print(repo._batches)

    data=repo.get("in-stock-batch1")
    # print(repo.list())
# test_repository_can_save_a_batch()