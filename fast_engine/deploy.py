from pathlib import Path
from .config import Config
from .utils import ensure_directory, logger


def deploy(config: Config) -> str:
    """Simple deploy function using the provided configuration."""
    output_dir = Path(config.output_path)
    ensure_directory(output_dir)
    logger.info("Deploying to %s", output_dir)
    return f"Deployed to {output_dir}"
