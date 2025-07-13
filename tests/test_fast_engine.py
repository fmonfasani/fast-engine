import fast_engine
from fast_engine.core import Engine, create_app


def test_version_exists():
    assert isinstance(fast_engine.__version__, str)


def test_engine_run():
    engine = Engine()
    assert engine.run() == "running"


def test_create_app():
    assert create_app() == "fast_engine_app"
