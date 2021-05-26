import abc
from domain import model


class AbstractRepository(abc.ABC):
    _batches = set()

    @abc.abstractmethod
    async def add(self, batch: model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, ref) -> model.Batch:
        raise NotImplementedError

    @property
    async def batches(self):
        return self._batches


class AbstractProductRepository(abc.ABC):
    _products = set()
    seen = set()

    async def add(self, product):
        await self._add(product)
        self.seen.add(product)

    async def get(self,sku) -> model.Product:
        product=await self._get(sku)
        if product:
            self.seen.add(product)
        return product

    async def get_by_batchref(self,batchref) -> model.Product:
        product= await self._get_by_batchref(batchref)
        if product:
            self.seen.add(product)
        return product

    @abc.abstractmethod
    async def _add(self, product:model.Product) :
        raise NotImplementedError

    @abc.abstractmethod
    async def _get(self, sku) -> model.Product:
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_by_batchref(self,batchref) -> model.Product:
        raise NotImplementedError

    @property
    async def products(self):
        return self._products
