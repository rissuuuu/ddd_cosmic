import json
import logging

import redis

from domain import commands
from service_layer import messagebus
from service_layer import unit_of_work

r = redis.Redis(host='127.0.0.1', port=6379)


def main():
    # orm.start_mappers()
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("hello")  # (1)

    for m in pubsub.listen():
        data=json.loads(m["data"].decode("utf-8"))
        task=data["task"]
        if task=="change_batch_quantity":
            handle_change_batch_quantity(task,data["event"])
        if task =="create_batch":
            handle_create_batch(task,data["event"])
        if task == "allocation_required":
            handle_allocate(task,data["event"])


def handle_change_batch_quantity(task,m):
    print("handling", task)
    data=m
    # data = json.loads(m['data'].decode("utf-8"))
    # data = json.loads(m["data"])  # (2)
    cmd = commands.ChangeBatchQuantity(
        ref=data["ref"], qty=data["qty"])  # (2)
    print(cmd)
    messagebus.handle(cmd, uow=unit_of_work.FakeUnitOfWork)

def handle_create_batch(task,m):
    print("handling", task)
    data=m
    print(data)
    command = commands.CreateBatch(ref=data["ref"], sku=data["sku"], qty=data["qty"])
    print(command)
    results = messagebus.handle(message=command,uow=unit_of_work.FakeUnitOfWork)

def handle_allocate(task,m):
    print("handling", task)
    data=m
    print(data)
    command = commands.Allocate(
        sku= data["sku"],
        qty= data["qty"]
    )
    print(command)
    results = messagebus.handle(message=command,uow=unit_of_work.FakeUnitOfWork)

if __name__ == "__main__":
    main()
