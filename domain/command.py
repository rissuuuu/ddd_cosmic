from pydantic import BaseModel
from domain import model
from typing import Optional
from datetime import date

class AddBatch(BaseModel):
    sku: str
    purchased_quantity: int


class AddOrderLine(BaseModel):
    sku: str
    qty: int