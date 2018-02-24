import click

from katsudon.cli import Command


class Migrate(Command):
    """
    Migrate the database.
    """
    cli_config = [
        click.option("-a", default=2, help="how many as")
    ]

    def __call__(self, a):
        self.warn("called! %s" % a)
