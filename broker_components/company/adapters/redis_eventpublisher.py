import json

import redis

from company_components.company.domain import events

r = redis.Redis(host="redis", port=6379)


async def publish(channel, event: events.Event):  # (1)
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe("task")
    r.publish("task",json.dumps({"task":channel,"event": event.json()}))

