from sanic import Blueprint, response

from broker_components.company.adapters import repository
from broker_components.company.views import views
from broker_components.company.service_layer import (
    unit_of_work,
    handlers,
    abstract,
)

company = Blueprint("company")


@company.route("/add_company", methods=["POST"])
async def add_company(request):
    company_name = request.form.get("company_name")
    company_symbol = request.form.get("company_symbol")
    sector = request.form.get("sector")
    listed_shares = request.form.get("listed_shares")
    paid_up_values = request.form.get("paid_up_values")
    total_paid_up_values = request.form.get("total_paid_up_values")
    company_ = abstract.AddCompany(
        company_name=company_name,
        company_symbol=company_symbol,
        sector=sector,
        listed_shares=listed_shares,
        paid_up_values=paid_up_values,
        total_paid_up_values=total_paid_up_values,
    )

    await handlers.add_company(
        validated_data=company_,
        uow=unit_of_work.CompanySqlAlchemyUnitOfWork(
            connection=request.app.ctx.db,
            repository_class=repository.SqlCompanyRepository,
        ),
    )
    return response.text("Company Added")


@company.route("/get_company", methods=["GET"])
async def get_company(request):
    company_symbol = request.form.get("company_symbol")

    company = await views.get_company(
        company_symbol,
        uow=unit_of_work.CompanySqlAlchemyUnitOfWork(
            connection=request.app.ctx.db,
            repository_class=repository.SqlCompanyRepository,
        ),
    )
    print(company)
    return response.text("GET Success")


@company.route("/get_all_company", methods=["GET"])
async def get_all_company(request):

    company = await views.get_all_companies(
        uow=unit_of_work.CompanySqlAlchemyUnitOfWork(
            connection=request.app.ctx.db,
            repository_class=repository.SqlCompanyRepository,
        )
    )
    print(company)
    return response.text("GET Success")


@company.route("/update_company", methods=["PUT"])
async def update_company(request):
    company_name = request.form.get("company_name")
    company_symbol = request.form.get("company_symbol")
    sector = request.form.get("sector")
    listed_shares = request.form.get("listed_shares")
    paid_up_values = request.form.get("paid_up_values")
    total_paid_up_values = request.form.get("total_paid_up_values")
    company_ = abstract.UpdateCompany(
        company_name=company_name,
        company_symbol=company_symbol,
        sector=sector,
        listed_shares=listed_shares,
        paid_up_values=paid_up_values,
        total_paid_up_values=total_paid_up_values,
    )

    await handlers.update_company(
        validated_data=company_,
        uow=unit_of_work.CompanySqlAlchemyUnitOfWork(
            connection=request.app.ctx.db,
            repository_class=repository.SqlCompanyRepository,
        ),
    )
    return response.text("Company Updated")
