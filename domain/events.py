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
    def json(self):
        return {
            "ref":self.ref,
            "sku":self.sku,
            "qty":self.qty
        }

@dataclass
class AllocationRequired(Event):
    orderid: str
    sku: str
    qty: int
    def json(self):
        return {
            "sku":self.sku,
            "qty":self.qty
        }

@dataclass
class BatchQuantityChanged(Event):
    ref: str
    qty: int
    def json(self):
        return {
            "ref":self.ref,
            "qty":self.qty
        }


@dataclass
class Allocated(Event):
    orderid: str
    sku: str
    qty: int
    batchref: str

    def json(self):
        return {
            "orderid":self.orderid,
            "sku":self.sku,
            "qty":self.qty,
            "batchref":self.batchref
        }