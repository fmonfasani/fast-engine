import sys
import types
from unittest import mock

# Provide minimal stubs so fast_engine can be imported without external deps
typer_mod = types.ModuleType('typer')

class DummyTyper:
    def __init__(self, *a, **k):
        pass
    def command(self, *a, **k):
        def decorator(func):
            return func
        return decorator
    def __call__(self, args=None):
        return None

typer_mod.Typer = DummyTyper
typer_mod.Argument = lambda *a, **k: None
typer_mod.Option = lambda *a, **k: None
typer_mod.Exit = type('Exit', (Exception,), {})
typer_mod.testing = types.ModuleType('typer.testing')
typer_mod.testing.CliRunner = object
rich_mod = types.ModuleType('rich')
rich_mod.print = print
rich_mod.console = types.ModuleType('rich.console')
rich_mod.console.Console = object
rich_mod.table = types.ModuleType('rich.table')
rich_mod.table.Table = object
sys.modules.setdefault('typer', typer_mod)
sys.modules.setdefault('typer.testing', typer_mod.testing)
sys.modules.setdefault('rich', rich_mod)
sys.modules.setdefault('rich.console', rich_mod.console)
sys.modules.setdefault('rich.table', rich_mod.table)

from fast_engine.utils import greet
from fast_engine.config import Config
import importlib


def test_greet():
    assert greet("Codex") == "Hello, Codex!"


def test_deploy(tmp_path, monkeypatch):
    cfg = mock.Mock(spec=Config)
    cfg.output_path = tmp_path
    called = False

    def fake_ensure(path):
        nonlocal called
        called = True

    deploy_module = importlib.import_module("fast_engine.deploy")
    monkeypatch.setattr(deploy_module, "ensure_directory", fake_ensure)
    result = deploy_module.deploy(cfg)
    assert called
    assert str(tmp_path) in result
