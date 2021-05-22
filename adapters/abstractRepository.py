import abc
from domain import model


class AbstractRepository(abc.ABC):
    _batches = set()

    @abc.abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, ref) -> model.Batch:
        raise NotImplementedError

    @property
    def batches(self):
        return self._batches


class AbstractProductRepository(abc.ABC):
    _products = set()
    seen = set()
    print("\n_______________________________________________seen________________________________________")
    print(seen)

    def add(self, product):
        self._add(product)
        self.seen.add(product)

    def get(self,sku) -> model.Product:
        product=self._get(sku)
        if product:
            self.seen.add(product)
        return product

    @abc.abstractmethod
    def _add(self, product:model.Product) :
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, sku) -> model.Product:
        raise NotImplementedError


    @property
    def products(self):
        return self._products
