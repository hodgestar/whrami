""" Whrami aiohttp app. """

from aiohttp import web


class IndexView(web.View):
    """ Top-level view. """
    async def get(self):
        return web.Response(body=b"Hello world.")


def create_app():
    """ Return an instance of the Whrami app. """
    app = web.Application()
    app.router.add_route('*', '/', IndexView)
    app.router.add_static('/static/', 'whrami/static/')
    return app
