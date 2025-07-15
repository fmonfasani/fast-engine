from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - fallback when PyYAML is missing
    yaml = None
from .utils import logger


@dataclass
class Template:
    """Template metadata"""

    name: str
    description: str
    version: str = "0.0.0"
    author: str = "Unknown"
    path: Optional[Path] = None

    @classmethod
    def from_file(cls, path: Path) -> "Template":
        if yaml:
            with open(path, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        else:
            data = {}
            with open(path, encoding="utf-8") as f:
                for line in f:
                    if ":" in line:
                        k, v = line.split(":", 1)
                        data[k.strip()] = v.strip()

        name = data.get("name")
        description = data.get("description")
        if not name or not description:
            raise ValueError("Template name and description are required")

        return cls(
            name=name,
            description=description,
            version=data.get("version", "0.0.0"),
            author=data.get("author", "Unknown"),
            path=path.parent,
        )

class TemplateEngine:
    """Motor de templates funcional"""
    
    def __init__(self, templates_path: str = "templates"):
        self.templates_path = Path(templates_path)
        
        if not self.templates_path.exists():
            self.templates_path.mkdir(parents=True, exist_ok=True)
    
    def render_project(self, template_name: str, context: Dict[str, Any]) -> Dict[str, str]:
        """Renderizar todos los archivos de un template"""
        logger.info(f"Renderizando template: {template_name}")
        
        files = self._create_basic_project(template_name, context)
        logger.info(f"Archivos generados: {len(files)}")
        return files
    
    def _create_basic_project(self, template_name: str, context: Dict[str, Any]) -> Dict[str, str]:
        """Crear proyecto basico funcional"""
        app_name = context.get("app_name", "my-app")
        app_description = context.get("app_description", f"Aplicacion SaaS: {app_name}")
        
        return {
            "README.md": f"""# {app_name}

{app_description}

Proyecto generado con Fast-Engine

## Quick Start

```bash
# Opcion 1: Local
pip install -r requirements.txt
python main.py

# Opcion 2: Docker
docker-compose up -d
```

## Endpoints

- GET / - Welcome message
- GET /health - Health check  
- GET /info - App information
- GET /docs - API documentation (Swagger UI)

## URLs

- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
""",
            
            "main.py": f"""from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="{app_name}",
    description="{app_description}",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {{
        "message": "Welcome to {app_name}!",
        "status": "running",
        "version": "1.0.0"
    }}

@app.get("/health")
def health_check():
    return {{
        "status": "healthy",
        "service": "{app_name}"
    }}

@app.get("/info")
def app_info():
    return {{
        "app_name": "{app_name}",
        "description": "{app_description}",
        "generated_by": "Fast-Engine",
        "endpoints": ["/", "/health", "/info", "/docs"]
    }}

if __name__ == "__main__":
    import uvicorn
    print("Starting {app_name}...")
    print("API Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
""",
            
            "requirements.txt": """fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
""",
            
            "Dockerfile": """FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
""",
            
            "docker-compose.yml": f"""services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - APP_NAME={app_name}
    restart: unless-stopped
  
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: {app_name.lower().replace('-', '_')}_db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
""",
            
            "run.py": f"""#!/usr/bin/env python3
import subprocess
import sys

def main():
    print("Starting {app_name}...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("Stopping {app_name}...")

if __name__ == "__main__":
    main()
""",
            
            ".gitignore": """__pycache__/
*.pyc
.env
*.log
.vscode/
.idea/
""",
            
            ".env.example": f"""APP_NAME={app_name}
DEBUG=true
ENV=development
DATABASE_URL=postgresql://user:password@localhost:5433/{app_name.lower().replace('-', '_')}_db
"""
        }
    
    def load_template_config(self, template_name: str) -> Template:
        """Load template metadata from template.yml"""
        path = self.templates_path / template_name / "template.yml"
        if not path.exists():
            raise FileNotFoundError(f"Template config not found: {template_name}")
        return Template.from_file(path)

    def list_templates(self) -> List[str]:
        """List available template names."""

        names: List[str] = []
        if not self.templates_path.exists():
            return names
        for item in self.templates_path.iterdir():
            if item.is_dir() and (item / "template.yml").exists():
                names.append(item.name)
        return sorted(names)