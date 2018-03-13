from types import ModuleType

settings = ModuleType('katsudon.conf.settings')

settings.apps = [
    'katsudon.apps.migrations',
    'katsudon.apps.http',
    'katsudon.apps.apps'
]

settings.http = ModuleType('katsudon.conf.settings.http')


settings.http.port = 8080
settings.http.host = "127.0.0.1"

from katsudon.apps.settings import load_settings
settings = load_settings()
