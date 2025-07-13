import fast_engine



def test_main():
    assert fast_engine.main() == "fast-engine works"

from fast_engine.core import FastEngine, create_app


def test_version_exists():
    assert isinstance(fast_engine.__version__, str)


def test_engine_run():
    engine = FastEngine()
    assert engine.run() == "running"


def test_create_app():
    assert create_app() == "fast_engine_app"

