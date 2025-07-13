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
    templates_path = package_dir.parent / "templates"
    
    if templates_path.exists():
        return str(templates_path)
    
    # Fallback para instalacion en site-packages
    fallback_path = package_dir / "templates"
    if fallback_path.exists():
        return str(fallback_path)
    
    # Ultimo fallback
    return "templates"

TEMPLATES_PATH = get_templates_path()

from .core import FastEngine
from .cli import app as cli_app
from .config import Config
from .deploy import deploy

__all__ = ["FastEngine", "cli_app", "Config", "TEMPLATES_PATH", "deploy"]
