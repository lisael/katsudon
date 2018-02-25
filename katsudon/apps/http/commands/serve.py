from aiohttp import web
import click

from katsudon.cli import Command
from katsudon.conf import settings
from katsudon.apps.apps.registry import Registry

class Serve(Command):
    """
    Run an http server
    """
    cli_config = [
        click.option("-h", "--host", default=settings.http.host),
        click.option("-p", "--port", default=settings.http.port),
    ]

    def add_routes(self):
        for app in Registry.apps:
            print(app.routes)
            for route in app.routes:
                self.app.router.add_get(*route)


    def __call__(self, host, port):
        self.app = web.Application()
        self.add_routes()
        web.run_app(self.app, host=host, port=port)
