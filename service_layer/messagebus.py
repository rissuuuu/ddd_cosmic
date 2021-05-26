import logging
from typing import Union, List

from domain import commands
from domain import events
from service_layer import unit_of_work
from service_layer import handlers

logger = logging.getLogger('werkzeug')

Message = Union[commands.Command, events.Event]


def handle(
        message: Message,
        uow: unit_of_work.FakeUnitOfWork):
    results = []
    queue = [message]
    while queue:
        message = queue.pop(0)
        if isinstance(message, events.Event):
            handle_event(message, queue, uow)
        elif isinstance(message, commands.Command):
            cmd_result = handle_command(message, queue, uow)
            results.append(cmd_result)
        else:
            raise Exception(f"{message} was not an event or command")
    return results


def handle_event(
        event: events.Event,
        queue: List[Message],
        uow: unit_of_work.FakeUnitOfWork
):
    for handler in EVENT_HANDLERS[type(event)]:
        try:
            logger.debug("handling event %s with handler %s", (event, handler))
            handler(event, uow=uow)
            queue.extend((uow().collect_new_events()))
        except Exception:
            logger.exception("Exception handling event %s", event)
            continue


def handle_command(
        command: commands.Command,
        queue: List[Message],
        uow: unit_of_work.FakeUnitOfWork,
):
    logger.debug("handling command %s", command)
    try:
        handler = COMMAND_HANDLERS[type(command)]
        result = handler(command= command, uow=uow)
        queue.extend(uow().collect_new_events())
        return result
    except:
        logger.exception("Exception handling command %s", command)
        raise


EVENT_HANDLERS = {
    events.Allocated: [handlers.publish_allocated_event],
    events.BatchQuantityChanged: [handlers.publish_batch_quantity_changed],
    events.OutOfStock: [handlers.send_out_of_stock_notification],
    events.BatchCreated: [handlers.publish_create_batch],
    events.AllocationRequired: [handlers.publish_allocation_required],
}

COMMAND_HANDLERS = {
    commands.Allocate: handlers.allocate,
    commands.CreateBatch: handlers.add_batch,
    commands.ChangeBatchQuantity: handlers.change_batch_quantity,
}
