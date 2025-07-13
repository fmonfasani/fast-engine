"""
Fast-Engine: Generador rapido de proyectos full-stack usando LLM APIs + Templates
"""

__version__ = "1.0.0"
__author__ = "Fast-Engine Team"

import os
from pathlib import Path

def get_templates_path():
    """Obtener path de templates"""
    package_dir = Path(__file__).parent

    # Primero buscar dentro del paquete instalado
    in_package = package_dir / "templates"
    if in_package.exists():
        return str(in_package)

    # Fallback para casos donde los templates estan junto al paquete
    sibling = package_dir.parent / "templates"
    if sibling.exists():
        return str(sibling)

    # Ultimo recurso: ruta relativa
    return "templates"

TEMPLATES_PATH = get_templates_path()


from .core import FastEngine, Engine, create_app
from .config import Config
from .deploy import deploy


try:
    from .cli import app as cli_app
except Exception:  # pragma: no cover - optional dependency may be missing
    cli_app = None

def main() -> str:
    """Entry point used in tests."""
    return "fast-engine works"

__all__ = [
    "FastEngine",
    "Engine",
    "create_app",
    "cli_app",
    "Config",
    "TEMPLATES_PATH",
    "main",
]

