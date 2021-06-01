from adapters import repository
from adapters.repository import FakeRepository, FakeProductRepository
from service_layer.abstract_unit_of_work import AbstractUnitOfWork


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, db=None):
        self.db_factory = db  # (1)

    def __enter__(self):
        self.db = self.db_factory()  # type: db  #(2)
        self.batches = repository.SqlAlchemyRepository(self.db)  # (2)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.db.close()  # (3)

    async def commit(self):  # (4)
        self.db.commit()

    async def rollback(self):  # (4)
        self.db.rollback()


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self,db):
        self.db = db
        self.committed = False

    def __enter__(self):
        print("\n_____________________Injected db___________________________\n",self.db,"\n")
        self.batches = FakeRepository._batches
        self.products = FakeProductRepository()
        return self

    async def _commit(self):
        self.committed = True

    def collect_new_events(self):
        self.products=FakeProductRepository()
        print("Seen",self.products.seen)
        for product in self.products.seen:
            while product.events:
                yield product.events.pop(0)


    async def rollback(self):
        pass
