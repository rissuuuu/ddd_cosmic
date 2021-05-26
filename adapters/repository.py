from typing import Set

from adapters.abstractRepository import AbstractRepository, AbstractProductRepository
from domain import model


class FakeRepository(AbstractRepository):
    def __init__(self):
        pass

    async def add(self, batch):
        self._batches.add(batch)

    async def get(self, reference):
        return next(b for b in self._batches if b.ref == reference)

    async def list(self):
        return self._batches


class FakeProductRepository(AbstractProductRepository):
    def __init__(self):
        super().__init__()

    async def _add(self, batch):
        self._products.add(batch)

    async def _get(self, sku):
        try:
            return next(p for p in self._products if p.sku == sku)
        except StopIteration:
            return None

    async def _get_by_batchref(self,batchref):
        return next((p for p in self._products for b in p.batches if str(b.ref)== batchref),None,)

    async def list(self):
        return self._products


class TrackingRepository:
    seen: Set[model.Product]

    def __init__(self, repo: AbstractRepository):
        self.seen = set()
        self._repo = repo

    async def add(self, product: model.Product):
        self._repo.add(product)
        self.seen.add(product)

    async def get(self, sku) -> model.Product:
        product = self._repo.get(sku)
        if product:
            self.seen.add(product)
        return product


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    async def add(self, batch):
        self.session.add(batch)

    async def get(self, reference):
        return self.session.query(model.Batch).filter_by(reference=reference).one()

    async def list(self):
        return self.session.query(model.Batch).all()

    async def _get_by_batchref(self, batchref):
        return (
            self.session.query(model.Product)
                .join(model.Batch)
                # .filter(orm.batches.c.reference == batchref)
                .first()
        )