from dataclasses import dataclass
from datetime import date
from typing import Optional

from pydantic import BaseModel


class Command:
    pass


class AddBatch(BaseModel):
    sku: str
    purchased_quantity: int


class AddOrderLine(BaseModel):
    sku: str
    qty: int


@dataclass
class Allocate(Command):
    sku: str
    qty: int


@dataclass
class CreateBatch(Command):
    ref: str
    sku: str
    qty: int
    eta: Optional[date] = None

@dataclass
class ChangeBatchQuantity(Command):
    ref: str
    qty: int

