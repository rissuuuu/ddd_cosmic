from __future__ import annotations
from typing import Any, Dict
from uuid import UUID, uuid4
from pydantic import BaseModel as Model


class Company(Model):
    id_: UUID
    company_name: str
    company_symbol: str
    sector: str
    listed_shares: str
    paid_up_values: float
    total_paid_up_values: str

    class Config:
        extra = "forbid"
        allow_mutation = False

    async def update(self, mapping: Dict[str, Any]) -> Company:
        return self.copy(update=mapping)


async def company_factory(
    company_name: str,
    company_symbol: str,
    sector: str,
    listed_shares: str,
    paid_up_values: float,
    total_paid_up_values: str,
) -> Company:
    return Company(
        id_=uuid4(),
        company_name=company_name,
        company_symbol=company_symbol,
        sector=sector,
        listed_shares=listed_shares,
        paid_up_values=paid_up_values,
        total_paid_up_values=total_paid_up_values,
    )
