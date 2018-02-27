# katsudon

An async web framework, based on aiohttp with Django-like composable apps.

## Features

### Django-like apps

### Django-like commands

Each app may define commands that are included in a project-wide cli tool.
Implemented with click.

### Django-like project and apps bootstraping

Implemented with cookiecutter

### Configuration management

Yaml files, unlike Django. Settings are namespaced per app and Katsudon
provides helper scripts to manage settings.

The settings system aims to be ops-friendly.

Not implemented, yet.

### Async-aware views

The views play well with async paradigm thanks to lazy contexts.

Not implemented yet.
