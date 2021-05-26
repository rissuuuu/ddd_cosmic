from uuid import uuid1, UUID
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List
from domain import events


class OrderLine(BaseModel):
    orderid: UUID
    sku: str
    qty: int

    def __hash__(self):
        return hash(self.orderid)


class Batch(BaseModel):
    ref: UUID
    sku: str
    eta: Optional[date]
    purchased_quantity: int
    allocations = set()

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.ref == self.ref

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def __lt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta < other.eta

    def __hash__(self):
        return hash(self.ref)

    async def allocate(self, line: OrderLine):
        if await self.can_allocate(line):
            self.allocations.add(line)

    async def deallocate(self, line: OrderLine):
        if line in self.allocations:
            self.allocations.remove(line)

    async def deallocate_one(self) -> OrderLine:
        return self.allocations.pop()

    @property
    async def allocated_quantity(self) -> int:
        return int(sum(line.qty for line in self.allocations))

    @property
    async def available_quantity(self) -> int:
        qty= await self.allocated_quantity
        return int(self.purchased_quantity) - int(qty)

    async def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and await self.available_quantity >= line.qty


async def BatchFactory(
        sku: str,
        purchased_quantity: int
) -> Batch:
    return Batch(
        ref=uuid1(),
        sku=sku,
        purchased_quantity=purchased_quantity,
        eta=datetime.now(),
        allocations=set()
    )


async def OrderLineFactory(
        sku: str,
        qty: int
) -> OrderLine:
    return OrderLine(
        orderid=uuid1(),
        sku=sku,
        qty=qty
    )


class Product(BaseModel):
    sku: str
    batches: List[Batch]
    events: List[events.Event]
    class Config:
        arbitrary_types_allowed=True

    def __hash__(self):
        return hash(self.sku)

    async def allocate(self, line: OrderLine) -> str:
        try:
            batch = next(b for b in sorted(self.batches) if b.can_allocate(line))
            print("\n______________________________________before available quantity____________________________________\n")
            print(await batch.available_quantity)
            await batch.allocate(line)
            print("\n______________________________________after available quantity____________________________________\n")
            print(await batch.available_quantity)
            allocated_event=(events.Allocated(
                orderid = str(line.orderid),
                sku = line.sku,
                qty = line.qty,
                batchref =  str(batch.ref)
            ))
            print("\n___________________________Event allocated____________________________\n",allocated_event)
            self.events.append(allocated_event)
            return str(batch.ref)
        except StopIteration:
            self.events.append(events.OutOfStock(sku=line.sku))
            # raise OutofStock(f"Out of stock for sku {line.sku}")
            return "None"
        finally:
            print(events)

    async def change_batch_quantity(self,ref: str, qty: int):
        batch = next(b for b in self.batches if str(b.ref)== ref)
        batch.purchased_quantity = qty
        while await batch.available_quantity < 0:
            line = await batch.deallocate_one()
            self.events.append(events.AllocationRequired(str(line.orderid),line.sku,line.qty))
        self.events.append(events.BatchQuantityChanged(ref = ref, qty = qty ))
        return "ok"

