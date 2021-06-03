import inspect
from typing import Callable

from databases import Database

from adapters import redis_eventpublisher
from service_layer import handlers
from service_layer import messagebus
from service_layer import unit_of_work


async def bootstrap(
        db : Database,
        publish: Callable = redis_eventpublisher.publish,
) -> messagebus.MessageBus:
    uow = unit_of_work.FakeUnitOfWork(db=db)
    dependencies = {"uow": uow, "publish": publish}
    injected_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies)
            for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }
    injected_command_handlers = {
         command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    data = messagebus.MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )
    return data


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)



