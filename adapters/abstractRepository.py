import abc
from domain import model

class AbstractRepository(abc.ABC):
    _batches=set()

    @abc.abstractmethod
    def add(self,batch:model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self,ref) -> model.Batch:
        raise NotImplementedError