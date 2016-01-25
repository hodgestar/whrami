""" Whrami aiohttp app. """

import aiohttp
from aiohttp import web
from . import events


class IndexView(web.View):
    """ Top-level view. """
    def get(self):
        return web.Response(body=b"Hello world.")


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.tp == aiohttp.MsgType.text:
            try:
                event = events.parse_event(msg.data)
            except:
                ws.send_str(events.close_web_socket.to_json())
                await ws.close()
                return ws
            if event.etype == 'close_web_socket':
                await ws.close()
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
    app.router.add_route('*', '/ws', websocket_handler)
    app.router.add_static('/static/', 'whrami/static/')
    return app
