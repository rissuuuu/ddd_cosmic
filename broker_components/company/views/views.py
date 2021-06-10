from broker_components.company.service_layer import unit_of_work
from broker_components.company.adapters.orm import  company

async def get_company(company_symbol: str, uow: unit_of_work.CompanySqlAlchemyUnitOfWork):
    async with uow:
        result = await uow.connection.fetch_one(
            query= company.select().where(company.c.company_symbol == company_symbol)
        )
    return result

async def get_all_companies(uow: unit_of_work.CompanySqlAlchemyUnitOfWork):
    async with uow:
        result = await uow.connection.fetch_all(
            query= company.select()
        )
    return result