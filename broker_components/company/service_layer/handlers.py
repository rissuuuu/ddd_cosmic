from __future__ import annotations, with_statement
from broker_components.company.service_layer import abstract
from broker_components.company.domain import command, model
from broker_components.company.service_layer import unit_of_work
from broker_components.company.service_layer import handler


async def add_company(
    validated_data: abstract.AddCompany,
    uow: unit_of_work.CompanySqlAlchemyUnitOfWork,
):
    async with uow:
        company = await handler.add_company(
            command.AddCompany(
                company_name=validated_data.company_name,
                company_symbol=validated_data.company_symbol,
                sector=validated_data.sector,
                listed_shares=validated_data.listed_shares,
                paid_up_values=validated_data.paid_up_values,
                total_paid_up_values=validated_data.total_paid_up_values,
            )
        )
        await uow.repository.add(company)


async def update_company(
    validated_data: abstract.UpdateCompany,
    uow: unit_of_work.CompanySqlAlchemyUnitOfWork,
):
    async with uow:
        company = await uow.repository.get(validated_data.company_symbol)
        company = model.Company(
            id_=company["id"],
            company_name=company["company_name"],
            company_symbol=company["company_symbol"],
            sector=company["sector"],
            listed_shares=company["listed_shares"],
            paid_up_values=company["paid_up_values"],
            total_paid_up_values=company["total_paid_up_values"],
        )

        company_values = await handler.update_company(
            command.UpdateCompany(
                company=company,
                listed_shares=validated_data.listed_shares
                if validated_data.listed_shares
                else company.listed_shares,
                paid_up_values=validated_data.paid_up_values
                if validated_data.paid_up_values
                else company.paid_up_values,
                total_paid_up_values=validated_data.total_paid_up_values
                if validated_data.total_paid_up_values
                else company.total_paid_up_values,
            )
        )
        await uow.repository.update(company_values)


COMMAND_HANDLERS = {
    command.AddCompany: add_company,
    command.UpdateCompany: update_company,
}

EVENT_HANDLERS = {}
