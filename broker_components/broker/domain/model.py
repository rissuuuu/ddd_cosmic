from __future__ import annotations
from typing import Any, Dict
from uuid import UUID, uuid4
from pydantic import BaseModel as Model


class Broker(Model):
    id_: UUID
    broker_id: int
    broker_name: str
    phone: str
    address: str

    class Config:
        extra = "forbid"
        allow_mutation = False
        title = "broker"

    async def update(self, mapping: Dict[str, Any]) -> Broker:
        return self.copy(update=mapping)


async def broker_factory(
    broker_id: int,
    broker_name: str,
    phone: str,
    address: str,
) -> Broker:
    return Broker(
        id_=uuid4(),
        broker_id=broker_id,
        broker_name=broker_name,
        phone=phone,
        address=address,
    )
