import inspect
from typing import Callable
from databases import Database
from service_layer import abstract_unit_of_work, unit_of_work
from service_layer import handlers
from service_layer import messagebus
from adapters import redis_eventpublisher
from ddd_cosmic import config


def init_database():
    pass


def bootstrap(
        uow: abstract_unit_of_work.AbstractUnitOfWork = unit_of_work.FakeUnitOfWork(db = init_database()),
        publish: Callable = redis_eventpublisher.publish,
) -> messagebus.MessageBus:
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



