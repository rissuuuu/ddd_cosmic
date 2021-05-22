from typing import Set

from adapters.abstractRepository import AbstractRepository, AbstractProductRepository
from domain import model


class FakeRepository(AbstractRepository):
    def __init__(self):
        pass

    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.ref == reference)

    def list(self):
        return self._batches


class FakeProductRepository(AbstractProductRepository):
    def __init__(self):
        pass

    def _add(self, batch):
        self._products.add(batch)

    def _get(self, sku):
        try:
            return next(p for p in self._products if p.sku == sku)
        except StopIteration:
            return None

    def list(self):
        return self._products


class TrackingRepository:
    seen: Set[model.Product]

    def __init__(self, repo: AbstractRepository):
        self.seen = set()
        self._repo = repo

    def add(self, product: model.Product):
        self._repo.add(product)
        self.seen.add(product)

    def get(self, sku) -> model.Product:
        product = self._repo.get(sku)
        if product:
            self.seen.add(product)
        return product


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.add(batch)

    def get(self, reference):
        return self.session.query(model.Batch).filter_by(reference=reference).one()

    def list(self):
        return self.session.query(model.Batch).all()
