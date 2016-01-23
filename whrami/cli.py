""" Whrami command line interface. """

import asyncio

import click

from .app import create_app


def run_app(app, host, port):
    """ Run an aiohttp application. """
    loop = asyncio.get_event_loop()
    handler = app.make_handler()
    f = loop.create_server(handler, host, port)
    srv = loop.run_until_complete(f)
    print('Web server listening on on', srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        loop.run_until_complete(handler.finish_connections(1.0))
        loop.run_until_complete(app.finish())
    loop.close()


@click.command("whrami")
@click.version_option()
@click.option(
    '--host', '-h',
    default='127.0.0.1',
    help='Host for web server to listen on')
@click.option(
    '--port', '-p',
    type=int, default=8000,
    help='Port for web server to listen on')
def main(host, port):
    """ Where am I?

        A text-based interactive fiction game.
        """
    app = create_app()
    run_app(app, host, port)
