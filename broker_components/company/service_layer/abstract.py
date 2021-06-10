from typing import Optional
from pydantic import BaseModel


class AddCompany(BaseModel):
    company_name: str
    company_symbol: str
    sector: str
    listed_shares: str
    paid_up_values: float
    total_paid_up_values: str


class UpdateCompany(BaseModel):
    company_name: Optional[str] = None
    company_symbol: Optional[str] = None
    sector: Optional[str] = None
    listed_shares: Optional[str] = None
    paid_up_values: Optional[float] = None
    total_paid_up_values: Optional[str] = None
