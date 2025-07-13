from .config import Config


def deploy(config: Config) -> str:
    """Simulate deploying an app."""
    return f"deploying {config.name}"
