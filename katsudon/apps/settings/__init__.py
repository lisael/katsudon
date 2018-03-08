from pyaml import dump
from io import StringIO

from katsudon.apps.settings.schema import Schema

def dumps(data):
    out = StringIO()
    dump(data, out)
    return out.getvalue()

def build_schema(*apps, name="katsudon.conf.settings"):
    s = Schema(name=name, data={})
    for app in apps:
        schema = app.find_data("settings.yml")
        if not schema.exists():
            continue
        with open(schema) as f:
            s.children[app.shortname] = Schema(app.shortname, yaml=f, parent=s)
    return s

def fetch_defaults(*apps):
    s = build_schema(*apps)
    import ipdb; ipdb.set_trace()
    return s.defaults()
