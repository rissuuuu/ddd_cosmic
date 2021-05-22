from domain import events


def handle(event: events.Event):
    for handler in HANDLERS[type(event)]:
        handler(event)

def sendmail(email,message):
    print("___________________________________________Event Triggered__________________________________________________")
    print(email,message)

def send_out_of_stock_notification(event: events.OutOfStock):
    sendmail(
        "email@email.com",
        f"out of stock {event.sku}"
    )


HANDLERS = {
    events.OutOfStock: [send_out_of_stock_notification],
}
