from types import ModuleType

settings = ModuleType('katsudon.settings')

settings.apps = ['katsudon.apps.migrations']
