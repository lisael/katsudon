import os
from os import path

import click

from cookiecutter.main import cookiecutter

from katsudon.cli import Command
from katsudon.conf import settings
from katsudon.apps.apps.registry import Registry
from katsudon.apps.settings import fetch_defaults, dumps


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
        app = Registry.current_app()

        tmpl_dir = app.find_data("cookiecutter", "project")

        apps_root = str(app.path.parent)

        available_apps = [
                dirname for dirname in os.listdir(apps_root)
                if path.isdir(path.sep.join([apps_root, dirname]))
                and not dirname.startswith("__")
        ]
        available_apps = Registry.apps
        default_settings = fetch_defaults(*available_apps)._as_dict()
        default_settings.setdefault("katsudon", {})["apps"] = [app.modname for app in Registry.apps]

        extra = dict(
            project_name = name,
            package_name = packagify(name),
            settings = dumps(default_settings),
        )
        cookiecutter(str(tmpl_dir), no_input=True, extra_context=extra)

