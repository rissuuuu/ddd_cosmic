from sanic import Sanic
from sanic import response

from domain import events
from service_layer import handlers, unit_of_work
from service_layer import messagebus

app = Sanic(__name__)


@app.get("/")
def hello_world(request):
    return response.text("hello How are you??")


@app.route("/send", methods=["POST"])
def add_batch(request):
    ref = request.form.get("ref")
    sku_ = request.form.get("sku")
    pq_ = request.form.get("purchased_quantity")
    event = events.BatchCreated(ref=ref, sku=sku_, qty=pq_)
    results = messagebus.handle(event=event,uow=unit_of_work.FakeUnitOfWork)
    # batch=handlers.add_batch(validated_data=abstract.AddBatch(
    #     sku = sku_,
    #     purchased_quantity = pq_
    # ),uow=unit_of_work.FakeUnitOfWork,
    # event=events.BatchCreated
    # )
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
    event = events.AllocationRequired(sku=sku, qty=qty, orderid=orderid)
    results = messagebus.handle(event, unit_of_work.FakeUnitOfWork)
    batchref = results.pop(0)
    return response.text(batchref)

@app.route("/change_batch_qty", methods=["POST"])
def change_batch_qty(request):
    ref = request.form.get("ref")
    qty = request.form.get("qty")
    event = events.BatchQuantityChanged(ref=ref, qty=qty)
    results=messagebus.handle(event,unit_of_work.FakeUnitOfWork)
    return  response.text(results.pop(0))

if __name__ == "__main__":
    app.run(auto_reload=True, debug=True, workers=4)
