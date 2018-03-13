import inspect

from katsudon.conf import settings

from .app import App


class Registry:
    apps = [App(app) for app in settings.katsudon.apps]
    app_by_name = None
    app_by_shortname = None

    @classmethod
    def commands(cls):
        return {app.shortname: app.commands
                for app in cls.apps if app.commands}

    @classmethod
    def current_app(cls):
        caller_fr = inspect.getouterframes(inspect.currentframe(), 2)[1]
        caller_mod = caller_fr.frame.f_globals["__name__"]
        for app in cls.apps:
            if caller_mod.startswith(app.modname):
                return app
        return None
