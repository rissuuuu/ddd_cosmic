import logging
from sanic import log
import logging
import redis
import json
from service_layer import messagebus
from domain import commands
from service_layer import unit_of_work


r = redis.Redis(host='0.0.0.0',port="6379")


def main():
    # orm.start_mappers()
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("change_batch_quantity")  # (1)

    for m in pubsub.listen():
        handle_change_batch_quantity(m)


def handle_change_batch_quantity(m):
    logging.debug("handling %s", m)
    data = json.loads(m["data"])  # (2)
    cmd = commands.ChangeBatchQuantity(
        ref=data["batchref"], qty=data["qty"])  # (2)
    messagebus.handle(cmd, uow=unit_of_work.FakeUnitOfWork)
