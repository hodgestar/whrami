""" Whrami aiohttp app. """

import asyncio
import os
import pkg_resources

import aiohttp
from aiohttp import web
from . import events

STATIC_FOLDER = pkg_resources.resource_filename(__name__, 'static')


class IndexView(web.View):
    """ Top-level view. """
    @asyncio.coroutine
    def get(self):
        index = os.path.join(STATIC_FOLDER, 'index.html')
        with open(index, 'rb') as f:
            body = f.read()
        return web.Response(body=body)


class WebSocketView(web.View):
    """ Websocket endpoint. """

    @asyncio.coroutine
    def get(self):
        ws = web.WebSocketResponse()
        yield from ws.prepare(self.request)

        while True:
            try:
                msg = yield from ws.receive()
            except web.WSClientDisconnectError:
                break
            if msg.tp == aiohttp.MsgType.text:
                try:
                    event = events.parse_event(msg.data)
                except:
                    ws.send_str(events.close_web_socket.to_json())
                    yield from ws.close()
                    return ws
                if event.etype == 'close_web_socket':
                    yield from ws.close()
                    return ws
                if event.etype == 'user_input':
                    ws.send_str(event.to_json())  # echo to client
                    ws.send_str(events.user_output("Got it.").to_json())
            elif msg.tp == aiohttp.MsgType.error:
                print('websocket connection closed with exception %s' %
                      ws.exception())

        print('websocket connection closed')
        return ws


def create_app():
    """ Return an instance of the Whrami app. """
    app = web.Application()
    app.router.add_route('*', '/', IndexView)
    app.router.add_route('*', '/ws', WebSocketView)
    app.router.add_static('/static/', STATIC_FOLDER)
    return app
