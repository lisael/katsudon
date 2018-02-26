from aiohttp import web

import click

from cookiecutter.main import cookiecutter

from katsudon.cli import Command
from katsudon.conf import settings
from katsudon.apps.apps.registry import Registry


def packagify(name):
    return name.strip().replace('-', "_")

class CreateProject(Command):
    """
    Create a Katsudon project
    """
    cli_config = [
        click.argument("name"),
    ]


    def __call__(self, name):
        tmpl_dir = Registry.current_app().find_data("cookiecutter", "project")
        extra = dict(
            project_name = name,
            package_name = packagify(name)
        )
        cookiecutter(str(tmpl_dir), no_input=True, extra_context=extra)
