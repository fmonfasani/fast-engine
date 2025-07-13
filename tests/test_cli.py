import importlib


def test_cli_version(cli_runner):
    import fast_engine.cli as cli
    importlib.reload(cli)
    result = cli_runner.invoke(cli.app, ["version"])
    assert result.exit_code == 0
    assert "Fast-Engine" in result.stdout
