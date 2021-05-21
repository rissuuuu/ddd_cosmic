from service_layer.abstract_unit_of_work import AbstractUnitOfWork
from adapters import repository
from adapters.repository import FakeRepository



class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=None):
        self.session_factory = session_factory  #(1)

    def __enter__(self):
        self.session = self.session_factory()  # type: Session  #(2)
        self.batches = repository.SqlAlchemyRepository(self.session)  #(2)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()  #(3)

    def commit(self):  #(4)
        self.session.commit()

    def rollback(self):  #(4)
        self.session.rollback()


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.committed = False  

    def __enter__(self):
        self.batches=FakeRepository._batches
        return self

    def commit(self):
        self.committed = True  

    def rollback(self):
        pass