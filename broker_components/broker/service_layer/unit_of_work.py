from lib import unit_of_work
from lib.db_connection import DbConnection
from broker_components.broker.adapters import repository
import typing


class BrokerSqlAlchemyUnitOfWork(unit_of_work.SqlAlchemyUnitOfWork):
    def __init__(
        self,
        connection: DbConnection,
        repository_class: typing.Type[repository.SqlBrokerRepository],
    ):
        super().__init__(connection, repository_class)
