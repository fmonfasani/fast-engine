import os
import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

@dataclass
class Config:
    """Configuracion de Fast-Engine"""
    openai_api_key: Optional[str] = None
    claude_api_key: Optional[str] = None
    deepseek_api_key: Optional[str] = None
    templates_path: str = None
    output_path: str = "."
    
    def __post_init__(self):
        if self.templates_path is None:
            from . import TEMPLATES_PATH
            self.templates_path = TEMPLATES_PATH
    
    @classmethod
    def load(cls, config_path: str = "fast-engine.json") -> "Config":
        """Cargar configuracion desde archivo o variables de entorno"""
        config_data = {}
        
        if Path(config_path).exists():
            try:
                with open(config_path, encoding='utf-8') as f:
                    config_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY", config_data.get("openai_api_key")),
            claude_api_key=os.getenv("CLAUDE_API_KEY", config_data.get("claude_api_key")),
            deepseek_api_key=os.getenv("DEEPSEEK_API_KEY", config_data.get("deepseek_api_key")),
            templates_path=config_data.get("templates_path"),
            output_path=config_data.get("output_path", ".")
        )
    
    def validate(self) -> bool:
        """Validar que las API keys estan configuradas"""
        return bool(self.openai_api_key and self.claude_api_key and self.deepseek_api_key)

    def save(self, config_path: str = "fast-engine.json"):
        """Guardar configuracion a archivo"""
        config_dict = {
            "openai_api_key": self.openai_api_key,
            "claude_api_key": self.claude_api_key, 
            "deepseek_api_key": self.deepseek_api_key,
            "templates_path": self.templates_path,
            "output_path": self.output_path
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2)
