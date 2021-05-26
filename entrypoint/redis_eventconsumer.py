import asyncio
import json

import redis

r = redis.Redis(host='127.0.0.1', port=6379)


async def main():
    # orm.start_mappers()
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("hello")  # (1)

    for m in pubsub.listen():
        print(m)
        data = json.loads(m["data"].decode("utf-8"))
        task = data["task"]
        if task == "change_batch_quantity":
            print("batch quantity changed")

        if task == "line_allocated":
            print("line is allocated and send message to all the units")


async def line_allocated():
    pass


async def batch_quantity_changed():
    pass


if __name__ == "__main__":
    asyncio.run(main())
