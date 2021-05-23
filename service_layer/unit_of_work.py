from adapters import repository
from adapters.repository import FakeRepository, FakeProductRepository
from service_layer.abstract_unit_of_work import AbstractUnitOfWork


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=None):
        self.session_factory = session_factory  # (1)

    def __enter__(self):
        self.session = self.session_factory()  # type: Session  #(2)
        self.batches = repository.SqlAlchemyRepository(self.session)  # (2)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()  # (3)

    def commit(self):  # (4)
        self.session.commit()

    def rollback(self):  # (4)
        self.session.rollback()


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.committed = False

    def __enter__(self):
        self.batches = FakeRepository._batches
        self.products = FakeProductRepository()
        return self

    def _commit(self):
        self.committed = True

    def collect_new_events(self):
        self.products=FakeProductRepository()
        print("Seen",self.products.seen)
        for product in self.products.seen:
            while product.events:
                yield product.events.pop(0)

    def rollback(self):
        pass
