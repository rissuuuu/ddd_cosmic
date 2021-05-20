from sanic import Sanic
from sanic.response import text
from service_layer import services
from service_layer import abstract
from sanic import response
import json
from flask import make_response,jsonify


app = Sanic(__name__)


@app.get("/")
def hello_world(request):
    return response.text("hello How are you??")


@app.route("/send", methods=['GET', 'POST'])
def add_batch(request):
    ref_ = request.form.get("ref")
    sku_ = request.form.get("sku")
    pq_ = request.form.get("purchased_quantity")
    batch=services.add_batch(validated_data=abstract.AddBatch(
        ref = ref_,
        sku = sku_,
        purchased_quantity = pq_
    ))
    return response.json(json.loads(batch))

@app.route("/get_data", methods=['GET', 'POST'])
def get_all_batches(request):
    batches=services.get_batches()
    return make_response(jsonify(batches))

if __name__ == "__main__":
    app.run(auto_reload=True, debug=True, workers=4)
