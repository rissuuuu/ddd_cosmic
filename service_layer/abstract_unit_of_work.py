import abc
from adapters import repository

class AbstractUnitOfWork(abc.ABC):

    def __exit__(self, *args):  #(2)
        self.rollback()  #(4)

    @abc.abstractmethod
    def commit(self):  #(3)
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):  #(4)
        raise NotImplementedError