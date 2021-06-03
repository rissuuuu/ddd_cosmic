from typing import Set

from adapters.abstractRepository import AbstractRepository, AbstractProductRepository
from adapters import orm
from domain import model


class FakeRepository(AbstractRepository):
    def __init__(self,db):
        self.db = db
        pass

    async def add(self, batch):
        await self.db.execute(
            query=orm.batches.insert().returning(orm.batches.c.ref),
            values={
                "ref" : str(batch.ref),
                "sku" : batch.sku,
                "purchased_qty" : batch.purchased_quantity

            },
        )
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

    async def _get_by_batchref(self, batchref):
        return next((p for p in self._products for b in p.batches if str(b.ref) == batchref), None,)

    async def list(self):
        return self._products


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, db):
        self.db = db

    async def add(self, batch):
        self.db.add(batch)

    async def get(self, reference):
        return self.db.query(model.Batch).filter_by(reference=reference).one()

    async def list(self):
        return self.db.query(model.Batch).all()

    async def _get_by_batchref(self, batchref):
        return (
            self.db.query(model.Product)
                .join(model.Batch)
            # .filter(orm.batches.c.reference == batchref)
                .first()
        )
