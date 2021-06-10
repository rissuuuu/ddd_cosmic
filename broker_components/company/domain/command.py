from pydantic import BaseModel
from broker_components.company.domain import model
from datetime import date


class Command(BaseModel):
    pass

class AddCompany(Command):
    company_name: str
    company_symbol:str
    sector: str
    listed_shares: str
    paid_up_values: float
    total_paid_up_values: str

class UpdateCompanyCommand(Command):
    company:model.Company

class UpdateCompany(UpdateCompanyCommand):
    listed_shares: str
    paid_up_values: float
    total_paid_up_values: str