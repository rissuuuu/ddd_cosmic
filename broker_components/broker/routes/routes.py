from sanic import Blueprint, response

from broker_components.broker.adapters import repository
from broker_components.broker.views import views
from broker_components.broker.service_layer import unit_of_work, handlers, abstract

broker = Blueprint("broker")


@broker.route("/", methods=["GET"])
async def test(request):
    print(request.app.ctx.db)
    return response.json({"Hello": "world from addy"})


@broker.route("/add_broker", methods=["POST"])
async def add_broker(request):
    broker_id = request.form.get("broker_id")
    broker_name = request.form.get("broker_name")
    phone = request.form.get("phone")
    address = request.form.get("address")
    abstrct = abstract.AddBroker(
        broker_id=broker_id,
        broker_name=broker_name,
        phone=phone,
        address=address,
    )
    uow = unit_of_work.BrokerSqlAlchemyUnitOfWork(
        connection=request.app.ctx.db, repository_class=repository.SqlBrokerRepository
    )
    await handlers.add_broker(validated_data=abstrct, uow=uow)
    return response.text("Broker Added")


@broker.route("/update_broker", methods=["PUT"])
async def update_broker(request):
    broker_id = request.form.get("broker_id")
    broker_name = request.form.get("broker_name")
    phone = request.form.get("phone")
    address = request.form.get("address")
    abstrct = abstract.UpdateBroker(
        broker_id=broker_id,
        broker_name=broker_name,
        phone=phone,
        address=address,
    )
    uow = unit_of_work.BrokerSqlAlchemyUnitOfWork(
        connection=request.app.ctx.db, repository_class=repository.SqlBrokerRepository
    )
    await handlers.update_broker(
        validated_data=abstrct,
        uow=uow,
    )
    return response.text("Broker Updated")


@broker.route("get_broker", methods=["GET"])
async def get_broker(request):
    broker_id = int(request.form.get("broker_id"))
    uow = unit_of_work.BrokerSqlAlchemyUnitOfWork(
        connection=request.app.ctx.db, repository_class=repository.SqlBrokerRepository
    )
    broker = await views.get_broker(broker_id, uow)
    print(broker)
    return response.text("GET Success")


@broker.route("get_all_broker", methods=["GET"])
async def get_all_broker(request):
    uow = unit_of_work.BrokerSqlAlchemyUnitOfWork(
        connection=request.app.ctx.db, repository_class=repository.SqlBrokerRepository
    )
    broker = await views.get_all_brokers(uow)
    print(broker)
    return response.text("GET Success")
