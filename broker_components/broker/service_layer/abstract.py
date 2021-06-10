from typing import Optional
from pydantic import BaseModel


class AddBroker(BaseModel):
    broker_id: int
    broker_name: str
    phone: str
    address: str


class UpdateBroker(BaseModel):
    broker_id: Optional[int] = None
    broker_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
