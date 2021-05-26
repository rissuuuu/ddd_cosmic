import json

import redis

from domain import events
from entrypoint import redis_eventconsumer

r = redis.Redis(host="127.0.0.1", port=6379)


async def publish(channel, event: events.Event):  # (1)
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe("hello")
    print(f"___________________________publishing: channel={channel}, event={event},redis={r}______________________\n")
    r.publish("hello",json.dumps({"task":channel,"event": event.json()}))

