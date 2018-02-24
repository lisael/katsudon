import os
import sys
import click
from colorama import Fore, Style
from pathlib import Path


CONTEXT_SETTINGS = dict(auto_envvar_prefix='KATSUDON')


class Context(object):

    def __init__(self):
        self.verbose = False
        self.settings = None


pass_context = click.make_pass_decorator(Context, ensure=True)


class Command:
    def __init__(self, verbose):
        self.verbose = verbose

    def echo(self, msg, *args, err=False, color=None):
        """Logs a message to stdout."""
        if args:
            msg %= args
        if color:
            msg = "%s%s%s" % (getattr(Fore, color.upper()), msg, Style.RESET_ALL)
        click.echo(msg, err=err)

    def err(self, msg, *args, color=None):
        "Log a message to stderr"
        self.echo(msg, *args, err=True, color=color)

    def vecho(self, msg, *args, color=None):
        """Logs a verbose message to stdout."""
        if self.verbose:
            self.echo(msg, *args, color=color)

    def success(self, msg, *args):
        """Logs a message to stdout, colored green"""
        if args:
            msg %= args
        self.echo(msg, color="green")

    def vsuccess(self, msg, *args):
        """Logs a verbose message to stdout, colored green"""
        if self.verbose:
            self.success(msg, *args)

    def warn(self, msg, *args):
        """Logs a message to stderr, colored yellow"""
        self.err(msg, *args, color="yellow")

    def vwarn(self, msg, *args):
        """Logs a message to stderr."""
        if self.verbose:
            self.warn(msg, *args)

    def error(self, msg, *args):
        """Logs a message to stderr."""
        self.err(msg, *args, color='red')

    def verror(self, msg, *args):
        """Logs a message to stderr."""
        if self.verbose:
            self.error(msg, *args)


class KatsudonSubCli(click.MultiCommand):
    "sub group of commands"
    def __init__(self, *args, **kwargs):
        self.module = None
        super(KatsudonSubCli, self).__init__(*args, **kwargs)

    def list_commands(self, ctx):
        root = Path(self.module.__file__).parent
        return [child[:-3] for child in os.listdir(root)
                if not child.startswith("__")
                and child.endswith(".py")]

    def get_command(self, ctx, name):
        mod = __import__(".".join([self.module.__name__, name]), None, None, [""])
        cmd_cls = [v for k, v in mod.__dict__.items()
                   if not k.startswith("_")
                   and isinstance(v, type)
                   and v is not Command
                   and Command in v.__mro__][0]

        @pass_context
        def cmd(ctx, *args, **kwargs):
            cmd_cls(verbose=ctx.verbose)(*args, **kwargs)

        for conf in cmd_cls.cli_config:
            cmd = conf(cmd)

        cmd = click.command()(cmd)
        cmd.short_help = cmd_cls.__doc__.lstrip()
        return cmd


class KatsudonCLI(click.MultiCommand):

    def __init__(self, *args, **kwargs):
        super(KatsudonCLI, self).__init__(*args, **kwargs)
        self.cmd_modules = {}

    def list_commands(self, ctx):
        from katsudon.conf import settings
        rv = []
        for app in settings.apps:
            try:
                mod = __import__(app + ".commands", None, None, [""])
                name = Path(mod.__file__).parent.parent.name
                self.cmd_modules[name] = mod
                rv.append(name)
            except:
                pass
        return rv

    def get_command(self, ctx, name):
        if not self.cmd_modules:
            self.list_commands(ctx)

        try:
            module = self.cmd_modules[name]
        except KeyError:
            raise click.ClickException("Sub command '%s' not found.\nTry `katsudon --help`" % name)

        @click.command(cls=KatsudonSubCli)
        @pass_context
        def grp(ctx):
            pass

        grp.short_help = module.__doc__.lstrip()
        grp.module = module
        return grp


@click.command(cls=KatsudonCLI, context_settings=CONTEXT_SETTINGS)
@click.option('--settings', type=click.File(), help='Settings file')
@click.option('-v', '--verbose', is_flag=True,
              help='Enables verbose mode.')
@pass_context
def cli(ctx, verbose, settings):
    """A complex command line interface."""
    ctx.verbose = verbose
    if settings is not None:
        os.environ["KATSUDON_SETTINGS"] = settings
