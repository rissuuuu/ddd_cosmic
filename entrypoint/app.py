import redis
import tracemalloc
from sanic import Sanic
from sanic import response
from entrypoint import bootstrap
from entrypoint import create_app
from domain import commands
from service_layer import unit_of_work, handlers

app = create_app(config_name="default")

tracemalloc.start()

r = redis.Redis(host='127.0.0.1', port=6379)

# utils create and get_bus()

@app.get("/")
async def hello_world(request):
    return response.text("hello How are you??")


@app.route("/send", methods=["POST"])
async def add_batch(request):
    ref = request.form.get("ref")
    sku_ = request.form.get("sku")
    pq_ = request.form.get("purchased_quantity")
    # event = events.BatchCreated(ref=ref, sku=sku_,qty=pq_)
    # results = messagebus.handle(event, unit_of_work.FakeUnitOfWork)
    # return response.text("ok")

    command = commands.CreateBatch(ref=ref, sku=sku_, qty=pq_)
    results = await app.ctx.bus.handle(message=command)
    return response.text("ok")

@app.route("/get_data", methods=["GET"])
async def get_all_batches(request):
    batches = await handlers.get_batches(uow=unit_of_work.FakeUnitOfWork())
    return response.text("ok")

@app.route("/allocate",methods=["POST"])
async def allocate(request):
    sku = request.form.get("sku")
    qty = request.form.get("qty")
    command = commands.Allocate(sku=sku, qty=qty)
    results = await app.ctx.bus.handle(message=command)
    # batchref = results.pop(0)
    return response.text("ok")

@app.route("/change_batch_qty", methods=["POST"])
async def change_batch_qty(request):
    ref = request.form.get("ref")
    qty = request.form.get("qty")
    command = commands.ChangeBatchQuantity(ref=ref, qty=qty)
    results = await app.ctx.bus.handle(command)
    # return  response.text(results.pop(0))
    return response.text("ok")


if __name__ == "__main__":
    # listen_()
    app.run(auto_reload=True, debug=True, workers=4)
