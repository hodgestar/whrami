""" Dispatcher for managing game messages. """

from . import events


class Dispatcher:
    def __init__(self, ws):
        self._ws = ws

    def event(self, event):
        handler = getattr(self, 'handle_%s' % event.etype, self.handle_error)
        return handler(event)

    def handle_error(self, event):
        print("Unknown event type {r}".format(event.etype))

    def handle_create_web_socket(self, event):
        print("Websocket created")

    def handle_close_web_socket(self, event):
        print("Websocket closed")

    def handle_user_input(self, event):
        self.send_response("Got it.")

    def send_event(self, event):
        self._ws.send_str(event.to_json())

    def send_response(self, response):
        self.send_event(events.user_output(response))
