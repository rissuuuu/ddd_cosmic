from dataclasses import dataclass


class Event:
    pass


@dataclass
class OutOfStock(Event):
    sku: str

    def __hash__(self):
        return hash(self.sku)