import json

from sanic import Sanic
from sanic import response
from service_layer import services,abstract,unit_of_work

app = Sanic(__name__)


@app.get("/")
def hello_world(request):
    return response.text("hello How are you??")


@app.route("/send", methods=["POST"])
def add_batch(request):
    sku_ = request.form.get("sku")
    pq_ = request.form.get("purchased_quantity")
    batch=services.add_batch(validated_data=abstract.AddBatch(
        sku = sku_,
        purchased_quantity = pq_
    ),uow=unit_of_work.FakeUnitOfWork)
    return response.json(json.loads(batch))

@app.route("/get_data", methods=["GET"])
def get_all_batches(request):
    batches=services.get_batches(uow=unit_of_work.FakeUnitOfWork)
    return response.json(batches)

@app.route("/get_single_data", methods=["GET"])
def get_one_batches(request):
    batches=services.get_batches()
    return response.json(batches)

@app.route("/allocate",methods=["POST"])
def allocate(request):
    sku=request.form.get("sku")
    qty= request.form.get("qty")
    batchrf=services.allocate(validated_data=abstract.AddOrderLine(
        sku=sku,
        qty=qty
    ))
    return response.text(batchrf)


if __name__ == "__main__":
    app.run(auto_reload=True, debug=True, workers=4)
