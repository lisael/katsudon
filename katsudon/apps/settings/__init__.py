import os
import sys
from pathlib import Path
import warnings

import yaml
from pyaml import dump
from io import StringIO

from katsudon.apps.settings.schema import Schema
from katsudon.apps.settings.exceptions import ConfigurationError
from katsudon.apps.apps.app import App


def dumps(data):
    out = StringIO()
    dump(data, out)
    return out.getvalue()


def build_schema(*apps, name="katsudon.conf.settings"):
    s = Schema(name=name, data={})
    apps += ("katsudon",)
    for app in apps:
        if isinstance(app, str):
            app = App(app)
        schema = app.find_data("settings.yml")
        if not schema.exists():
            continue
        with open(schema) as f:
            s.children[app.shortname] = Schema(app.shortname, yaml=f, parent=s)
    return s


def fetch_defaults(*apps):
    s = build_schema(*apps)
    return s.defaults()


def load_settings():
    cmd_name = os.path.basename(sys.argv[0])
    settings_env_var = cmd_name.upper() + "_SETTINGS"
    settings_file = None
    if settings_env_var in os.environ:
        settings_file = Path(os.environ[settings_env_var])
    else:
        basename = "%s.yml" % cmd_name
        for path in [Path("/etc"),
                     Path().home(), Path.home().joinpath(".config")]:
            settings_file = path.joinpath(basename)
            if path.joinpath(basename).is_file():
                break
            elif path.joinpath(".%s" % basename).is_file():
                break
            else:
                settings_file = None
        if settings_file is None:
            settings_file = Path().cwd().joinpath("settings", "default.yml")
            if not settings_file.is_file():
                raise ConfigurationError(
                        'No settings file\n'
                        'Either provide --settings argument, %s env var,'
                        '/etc/%s.yml or ~/.%s.yml' % (
                            settings_env_var, cmd_name, cmd_name))
            warn_msg = 'Using default settings file. ' \
                       'Either provide --settings argument, %s env var,' \
                       '/etc/%s.yml or ~/.%s.yml' % (settings_env_var,
                                                     cmd_name, cmd_name)
            warnings.warn(warn_msg)
    with open(settings_file) as f:
        data = yaml.load(f)
        settings = fetch_defaults(*data["katsudon"]["apps"])
        print(settings._as_dict())
        settings._update(data)
    print(settings._as_dict())
    return settings
