from dataclasses import dataclass
from typing import Optional
from datetime import date

class Event:
    pass


@dataclass
class OutOfStock(Event):
    sku: str

    def __hash__(self):
        return hash(self.sku)

@dataclass
class BatchCreated(Event):
    ref: str
    sku: str
    qty: int
    eta: Optional[date] = None

@dataclass
class AllocationRequired(Event):
    orderid: str
    sku: str
    qty: int