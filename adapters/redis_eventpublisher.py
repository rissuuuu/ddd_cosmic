import json
import redis
import logging
from domain import events
from attr import asdict


r = redis.Redis(host="0.0.0.0",port="6379")


def publish(channel, event: events.Event):  #(1)
    logging.debug("publishing: channel=%s, event=%s", channel, event)
    r.publish(channel, json.dumps(asdict(event)))