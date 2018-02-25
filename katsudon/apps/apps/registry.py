from pathlib import Path

from katsudon.conf import settings


class App:
    def __init__(self, modname):
        self.modname = modname
        self.shortname = modname.split(".")[-1]
        self.module = self.submodule()
        self._commands = None
        self._routes = None

    def submodule(self, *parts, froms=None):
        if froms is None:
            froms = [""]
        try:
            return __import__(".".join((self.modname,) + parts),
                              None, None, froms)
        except ImportError:
            return None

    @property
    def commands(self):
        if self._commands is None:
            cmdmod = self.submodule("commands")
            root = Path(self.cmdmod.__file__).parent
            cmd_names = [child[:-3] for child in os.listdir(root)
                         if not child.startswith("__")
                         and child.endswith(".py")]
            self._commands = {name: self.submodule("commands", name)
                              for name in cmd_names}
        return self._commands

    @property
    def routes(self):
        if self._routes is None:
            routes = self.submodule("routes")
            print(routes)
            if routes is None:
                self._routes = []
            else:
                print(routes.routes)
                self._routes = routes.routes
        return self._routes


class Registry:
    apps = [App(app) for app in settings.apps]

    @classmethod
    def commands(cls):
        return {app.shortname: app.commands
                for app in cls.apps if app.commands}
