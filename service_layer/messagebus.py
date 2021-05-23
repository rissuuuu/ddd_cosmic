from domain import events
from service_layer import unit_of_work,handlers


def handle(
        event: events.Event,
        uow: unit_of_work.FakeUnitOfWork):
    uw= uow
    results = []
    queue = [event]
    while queue:
        event = queue.pop(0)
        for handle in HANDLERS[type(event)]:
            results.append(handle(event=event, uow=uow))
            queue.extend(uw().collect_new_events())
    return results

HANDLERS = {
    events.BatchCreated: [handlers.add_batch],
    events.AllocationRequired: [handlers.allocate],
    events.OutOfStock: [handlers.send_out_of_stock_notification],
    events.BatchQuantityChanged: [handlers.change_batch_quantity]
}
