from broker_components.company.domain import model
from broker_components.company.domain import command


async def add_company(cmd: command.AddCompany) -> model.Company:
    return await model.company_factory(
        company_name=cmd.company_name,
        company_symbol=cmd.company_symbol,
        sector=cmd.sector,
        listed_shares=cmd.listed_shares,
        paid_up_values=cmd.paid_up_values,
        total_paid_up_values=cmd.total_paid_up_values,
    )


async def update_company(cmd: command.UpdateCompanyCommand) -> model.Company:
    if isinstance(cmd, command.UpdateCompany):
        return await cmd.company.update(
            {
                "listed_shares": cmd.listed_shares,
                "paid_up_values": cmd.paid_up_values,
                "total_paid_up_values": cmd.total_paid_up_values,
            }
        )
