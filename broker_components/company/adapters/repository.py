from lib.repository import Repository, SqlAlchemyRepository
from lib.repository import DbConnection
from broker_components.company.domain import model
from broker_components.company.adapters.orm import company


class CompanyRepository(Repository):
    async def add(self, model):
        return await super().add(model)

    async def get(self, ref):
        return await super().get(ref)


class SqlCompanyRepository(SqlAlchemyRepository):
    def __init__(self, db: DbConnection):
        self.db = db

    async def add(self, model: model.Company):
        await self.db.execute(
            query=company.insert(),
            values={
                "id": str(model.id_),
                "company_name": model.company_name,
                "company_symbol": model.company_symbol,
                "sector": model.sector,
                "listed_shares": model.listed_shares,
                "paid_up_values": model.paid_up_values,
                "total_paid_up_values": model.total_paid_up_values,
            },
        )

    async def get(self, ref: str):
        return await self.db.fetch_one(
            query=company.select().where(company.c.company_symbol == ref),
        )

    async def get_all_company(self):
        return await self.db.fetch_all(query=company.select())

    async def update(self, model: model.Company):
        await self.db.execute(
            query=company.update().where(company.c.id == str(model.id_)),
            values={
                "company_name": model.company_name,
                "sector": model.sector,
                "company_symbol": model.company_symbol,
                "listed_shares": model.listed_shares,
                "paid_up_values": model.paid_up_values,
                "total_paid_up_values": model.total_paid_up_values,
            },
        )
