import typing
from lib import unit_of_work
from lib.db_connection import DbConnection
from broker_components.company.adapters import repository


class CompanySqlAlchemyUnitOfWork(unit_of_work.SqlAlchemyUnitOfWork):
    def __init__(
        self,
        connection: DbConnection,
        repository_class: typing.Type[repository.SqlCompanyRepository],
    ):
        super().__init__(connection, repository_class)
