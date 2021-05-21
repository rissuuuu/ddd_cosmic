from uuid import uuid1,UUID
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List


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

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self.allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self.allocations:
            self.allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self.allocations)

    @property
    def available_quantity(self) -> int:
        return self.purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    batch = next(b for b in sorted(batches) if b.can_allocate(line))
    batch.allocate(line)
    return batch.ref


def BatchFactory(
    sku: str,
    purchased_quantity: int
) -> Batch:

    return Batch(
        ref = uuid1(),
        sku = sku,
        purchased_quantity = purchased_quantity,
        eta = datetime.now(),
        allocations = set()
    )

def OrderLineFactory(
    sku: str,
    qty: int
    ) -> OrderLine:
    return OrderLine(
        orderid=uuid1(),
        sku = sku,
        qty = qty
    )
