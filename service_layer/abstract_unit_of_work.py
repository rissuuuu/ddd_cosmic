import abc
from adapters import repository


class AbstractUnitOfWork(abc.ABC):

    def __exit__(self, *args):  # (2)
        self.rollback()  # (4)

    def commit(self):  # (3)
        self._commit()
        self.collect_new_events()

    @abc.abstractmethod
    def collect_new_events(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):  # (4)
        raise NotImplementedError

    @abc.abstractmethod
    def _commit(self):  # (3)
        raise NotImplementedError