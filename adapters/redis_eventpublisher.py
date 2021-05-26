import json

import redis

from domain import events
from entrypoint import redis_eventconsumer

r = redis.Redis(host="127.0.0.1", port=6379)


def publish(channel, event: events.Event):  # (1)
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe("hello")
    print(f"___________________________publishing: channel={channel}, event={event},redis={r}______________________\n")
    r.publish("hello",json.dumps({"task":channel,"event": event.json()}))
    # for m in p.listen():
    #     redis_eventconsumer.handle_change_batch_quantity(m)
#
#
# def handle_change_batch_quantity(m):
#     logging.debug("handling %s", m)
#     data = json.loads(m['data'].decode("utf-8"))
#     # data = json.loads(m["data"])  # (2)
#     cmd = commands.ChangeBatchQuantity(
#         ref=data["ref"], qty=data["qty"])  # (2)
#     messagebus.handle(cmd, uow=unit_of_work.FakeUnitOfWork)
