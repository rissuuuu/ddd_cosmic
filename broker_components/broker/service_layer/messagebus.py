import logging
from typing import Union, List, Dict, Type, Callable

from broker_components.broker.domain import command, events
from lib import unit_of_work

logger = logging.getLogger("werkzeug")

Message = Union[command.Command, events.Event]


class MessageBus:
    def __init__(
        self,
        uow: unit_of_work.SqlAlchemyUnitOfWork,
        event_handlers: Dict[Type[events.Event], List[Callable]],
        command_handlers: Dict[Type[command.Command], Callable],
    ):
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers

    async def handle(self, message: Message):
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, events.Event):
                await self.handle_event(message)
            elif isinstance(message, command.Command):
                await self.handle_command(message)
            else:
                raise Exception(f"{message} was not an Event or Command")

    async def handle_event(self, event: events.Event):
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug(
                    "handling event %s with handler %s",
                    event,
                    handler,
                )
                await handler(event)
                self.queue.extend(self.uow.collect_new_events())
            except Exception:
                logger.exception("Exception handling event %s", event)
                continue

    async def handle_command(self, command: command.Command):
        logger.debug("handling command %s", command)
        try:
            handler = self.command_handlers[type(command)]
            await handler(command)
            self.queue.extend(self.uow.collect_new_events())
        except Exception:
            logger.exception("Exception handling command %s", command)
            raise
