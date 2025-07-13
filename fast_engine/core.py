import json
import time
import os
from pathlib import Path
from typing import Dict, Any, Optional
from .config import Config
from .templates import TemplateEngine
from .utils import ensure_directory, logger
from .app import create_app as _create_app


def create_app() -> str:
    """Return an application object.

    This simple implementation just returns a placeholder string so
    tests can import and use it without requiring additional
    dependencies.
    """
    return "fast_engine_app"

class FastEngine:
    """Orquestador principal de Fast-Engine"""
    
    def __init__(self, config_path: str = "fast-engine.json"):
        self.config = Config.load(config_path)
        self.template_engine = TemplateEngine(self.config.templates_path)

    def create_app(self):
        """Return a basic application instance."""
        return _create_app()
    
    def init_project_demo(self, name: str, template: str = "saas-basic", description: str = "") -> str:
        """Demo de generacion de proyecto (sin APIs reales)"""
        logger.info(f"[ROCKET] Iniciando generacion de proyecto: {name}")
        
        print(f"[BRAIN] Simulando llamada a Claude para arquitectura...")
        time.sleep(1)
        
        print(f"[GEAR] Simulando llamada a OpenAI para backend...")
        time.sleep(1)
        
        print(f"[ART] Simulando llamada a DeepSeek para frontend...")
        time.sleep(1)
        
        # Simular contexto de generacion
        context = {
            "app_name": name,
            "app_description": description or f"Aplicacion SaaS: {name}",
            "architecture": {
                "entities": ["User", "Project", "Task"],
                "features": ["authentication", "project_management", "task_tracking"]
            },
            "generated_backend": "# FastAPI backend code generated...",
            "generated_frontend": "// Next.js frontend code generated..."
        }
        
        # Renderizar templates
        print(f"[DOCUMENT] Renderizando templates...")
        project_files = self.template_engine.render_project(template, context)
        
        print(f"[FLOPPY] Escribiendo archivos del proyecto...")
        print(f"[FOLDER] Archivos a crear: {len(project_files)}")
        
        # Debug: mostrar que archivos se van a crear
        for file_path in project_files.keys():
            print(f"  - {file_path}")
        
        # Escribir archivos con debugging
        self._write_project(name, project_files)
        
        return f"[CHECK] Proyecto {name} creado exitosamente en ./{name}/"
    
    def _write_project(self, name: str, files: Dict[str, str]):
        """Escribir archivos del proyecto al filesystem"""
        # Usar path absoluto del directorio actual
        current_dir = Path.cwd()
        project_path = current_dir / name
        
        print(f"[FOLDER] Directorio base: {current_dir}")
        print(f"[FOLDER] Directorio del proyecto: {project_path}")
        
        # Crear directorio del proyecto
        try:
            project_path.mkdir(exist_ok=True)
            print(f"[CHECK] Directorio creado: {project_path}")
        except Exception as e:
            print(f"[X] Error creando directorio: {e}")
            return
        
        # Escribir cada archivo
        files_created = 0
        for file_path, content in files.items():
            full_path = project_path / file_path
            
            try:
                # Crear directorios padre si no existen
                ensure_directory(full_path.parent)
                
                # Escribir archivo
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"[CHECK] Creado: {file_path}")
                files_created += 1
                
            except Exception as e:
                print(f"[X] Error creando {file_path}: {e}")
        
        print(f"[CHART] Total archivos creados: {files_created}/{len(files)}")
    
    def doctor(self) -> Dict[str, Any]:
        """Diagnostico del sistema"""
        current_path = Path.cwd()
        templates_path = Path(self.config.templates_path)
        
        status = {
            "config_valid": self.config.validate(),
            "api_keys": {
                "openai": bool(self.config.openai_api_key),
                "claude": bool(self.config.claude_api_key),
                "deepseek": bool(self.config.deepseek_api_key)
            },
            "templates_path": templates_path.exists(),
            "available_templates": self.template_engine.list_templates(),
            "current_directory": str(current_path),
            "output_path": self.config.output_path,
            "templates_absolute_path": str(templates_path.absolute()),
            "can_write": current_path.is_dir() and os.access(current_path, os.W_OK)
        }
        return status
        
class Engine:
    def run(self):
        return "running"

    def create_app():
        return "fast_engine_app"


# Expose the app factory at module level
create_app = _create_app
