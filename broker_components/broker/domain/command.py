from pydantic import BaseModel
from broker_components.broker.domain import model


class Command(BaseModel):
    pass


class AddBroker(Command):
    broker_id: int
    broker_name: str
    phone: str
    address: str


class UpdateBrokerCommand(Command):
    broker: model.Broker


class UpdateBroker(UpdateBrokerCommand):
    broker_name: str
    phone: str
    address: str
