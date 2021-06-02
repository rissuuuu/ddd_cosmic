import tracemalloc

import redis
from sanic import response

from domain import commands
from entrypoint import create_app
from service_layer import unit_of_work, handlers
from utils import utils

app = create_app()
bus = utils.get_bootstrap(app)

tracemalloc.start()

r = redis.Redis(host='127.0.0.1', port=6379)

@app.main_process_start
async def start_db(app,loop):
    print("DB connected")
    await app.ctx.db.connect()

@app.main_process_stop
async def stop_db(app,loop):
    print("DB Disconnected")
    # await app.ctx.db.disconnect()
    
@app.get("/")
async def hello_world(request):
    return response.text("hello How are you??")


@app.route("/send", methods=["POST"])
async def add_batch(request):
    ref = request.form.get("ref")
    sku_ = request.form.get("sku")
    pq_ = request.form.get("purchased_quantity")
    command = commands.CreateBatch(ref=ref, sku=sku_, qty=pq_)
    results = await bus.handle(message=command)
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
    results = await bus.handle(message=command)
    return response.text("ok")

@app.route("/change_batch_qty", methods=["POST"])
async def change_batch_qty(request):
    ref = request.form.get("ref")
    qty = request.form.get("qty")
    command = commands.ChangeBatchQuantity(ref=ref, qty=qty)
    results = await bus.handle(command)
    return response.text("ok")


if __name__ == "__main__":
    # listen_()
    app.run(auto_reload=True, debug=True, workers=4)
