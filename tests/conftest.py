import sys
import types
import io
import contextlib
import pytest

class DummyTyper:
    def __init__(self, help=None):
        self.commands = {}
    def command(self, *args, **kwargs):
        def decorator(func):
            name = func.__name__.replace('_', '-')
            self.commands[name] = func
            return func
        return decorator
    def __call__(self, args=None):
        args = list(args or [])
        if not args:
            return
        cmd = args.pop(0)
        func = self.commands[cmd]
        return func()

def Argument(default=None, *args, **kwargs):
    return default

def Option(default=None, *args, **kwargs):
    return default

class Exit(Exception):
    def __init__(self, code=0):
        self.code = code

class DummyCliRunner:
    def invoke(self, app, args=None):
        out = io.StringIO()
        try:
            with contextlib.redirect_stdout(out):
                app(args)
            return types.SimpleNamespace(exit_code=0, stdout=out.getvalue())
        except Exit as e:
            return types.SimpleNamespace(exit_code=e.code, stdout=out.getvalue())

@pytest.fixture
def cli_runner(monkeypatch):
    typer_mod = types.ModuleType('typer')
    testing_mod = types.ModuleType('typer.testing')
    typer_mod.Typer = DummyTyper
    typer_mod.Argument = Argument
    typer_mod.Option = Option
    typer_mod.Exit = Exit
    testing_mod.CliRunner = DummyCliRunner
    typer_mod.testing = testing_mod

    rich_mod = types.ModuleType('rich')
    console_mod = types.ModuleType('rich.console')
    table_mod = types.ModuleType('rich.table')

    class Console:
        def print(self, *args, **kwargs):
            print(*args, **kwargs)
    class Table:
        def __init__(self, *a, **kw):
            pass
        def add_column(self, *a, **kw):
            pass
        def add_row(self, *a, **kw):
            pass

    console_mod.Console = Console
    table_mod.Table = Table
    def rprint(*args, **kwargs):
        print(*args, **kwargs)
    rich_mod.print = rprint
    rich_mod.console = console_mod
    rich_mod.table = table_mod

    monkeypatch.setitem(sys.modules, 'typer', typer_mod)
    monkeypatch.setitem(sys.modules, 'typer.testing', testing_mod)
    monkeypatch.setitem(sys.modules, 'rich', rich_mod)
    monkeypatch.setitem(sys.modules, 'rich.console', console_mod)
    monkeypatch.setitem(sys.modules, 'rich.table', table_mod)

    yield DummyCliRunner()

    # Clean up modules
    for name in ['typer', 'typer.testing', 'rich', 'rich.console', 'rich.table']:
        sys.modules.pop(name, None)
