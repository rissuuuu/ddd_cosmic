from sanic import Sanic
from sanic import response

from domain import events,commands
from service_layer import handlers, unit_of_work, messagebus

app = Sanic(__name__)


@app.get("/")
def hello_world(request):
    return response.text("hello How are you??")


@app.route("/send", methods=["POST"])
def add_batch(request):
    ref = request.form.get("ref")
    sku_ = request.form.get("sku")
    pq_ = request.form.get("purchased_quantity")
    command = commands.CreateBatch(ref=ref, sku=sku_, qty=pq_)
    results = messagebus.handle(message=command,uow=unit_of_work.FakeUnitOfWork)
    return response.text("ok")

@app.route("/get_data", methods=["GET"])
def get_all_batches(request):
    batches = handlers.get_batches(uow=unit_of_work.FakeUnitOfWork)
    return response.text("ok")

@app.route("/get_single_data", methods=["GET"])
def get_one_batches(request):
    batches = handlers.get_batches()
    return response.text("ok")

@app.route("/allocate",methods=["POST"])
def allocate(request):
    sku = request.form.get("sku")
    qty = request.form.get("qty")
    orderid = request.form.get("orderid")
    command = commands.Allocate(sku=sku, qty=qty)
    results = messagebus.handle(message=command, uow=unit_of_work.FakeUnitOfWork)
    batchref = results.pop(0)
    return response.text(batchref)

@app.route("/change_batch_qty", methods=["POST"])
def change_batch_qty(request):
    ref = request.form.get("ref")
    qty = request.form.get("qty")
    command = commands.ChangeBatchQuantity(ref=ref, qty=qty)
    results=messagebus.handle(command,unit_of_work.FakeUnitOfWork)
    return  response.text(results.pop(0))

if __name__ == "__main__":
    app.run(auto_reload=True, debug=True, workers=4)
