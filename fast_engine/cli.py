import os
from pathlib import Path
from typing import Optional

import typer
from jinja2 import Environment, FileSystemLoader
from rich import print as rprint
from rich.console import Console
from rich.table import Table


from .core import FastEngine

FAST_ENGINE_HOME = Path(os.environ.get("FAST_ENGINE_HOME", Path.home() / ".fast-engine"))

def get_templates_dir() -> Path:
    """Return directory containing built-in templates."""
    return Path(__file__).resolve().parent.parent / "templates"

def ensure_home() -> Path:
    """Ensure FAST_ENGINE_HOME exists and return it."""
    FAST_ENGINE_HOME.mkdir(parents=True, exist_ok=True)
    return FAST_ENGINE_HOME

app = typer.Typer(help="Fast-Engine: Generador rapido de proyectos full-stack")
console = Console()

@app.command()
def init(
    name: str = typer.Argument(..., help="Nombre del proyecto"),
    template: Optional[str] = typer.Option(None, "--template", "-t", help="Template a usar"),
):
    """Crear un nuevo proyecto a partir de un template"""
    templates_dir = get_templates_dir()
    available = [p.name for p in templates_dir.iterdir() if p.is_dir()]

    if not available:
        rprint("[red]No hay templates disponibles[/red]")
        raise typer.Exit(1)

    if not template:
        rprint("[cyan]Templates disponibles:[/cyan]")
        for idx, t_name in enumerate(available, 1):
            rprint(f"  {idx}. {t_name}")
        choice = typer.prompt("Selecciona template", type=int)
        if 1 <= choice <= len(available):
            template = available[choice - 1]
        else:
            rprint("[red]Opcion invalida[/red]")
            raise typer.Exit(1)
    elif template not in available:
        rprint(f"[red]Template '{template}' no encontrado[/red]")
        raise typer.Exit(1)

    env = Environment(loader=FileSystemLoader(str(templates_dir / template)), keep_trailing_newline=True)
    project_dir = ensure_home() / name
    project_dir.mkdir(parents=True, exist_ok=True)

    for src in (templates_dir / template).rglob('*'):
        if src.is_file():
            rel = src.relative_to(templates_dir / template)
            dest = project_dir / rel
            if dest.suffix == '.j2':
                dest = dest.with_suffix('')
                template_obj = env.get_template(str(rel))
                content = template_obj.render(project_name=name)
            else:
                content = src.read_text()
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content)

    rprint(f"[green]Proyecto creado en {project_dir}[/green]")

@app.command()
def doctor():
    """Diagnostico del sistema"""
    try:
        engine = FastEngine()
        status = engine.doctor()
        
        table = Table(title="Fast-Engine Doctor")
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Details")
        
        config_status = "[CHECK] OK" if status["config_valid"] else "[X] ERROR"
        table.add_row("Configuration", config_status, "API keys configured" if status["config_valid"] else "Missing API keys")
        
        for api, configured in status["api_keys"].items():
            status_text = "[CHECK] SET" if configured else "[X] MISSING"
            table.add_row(f"  {api.upper()}_API_KEY", status_text, "")
        
        templates_status = "[CHECK] OK" if status["templates_path"] else "[X] NOT FOUND"
        templates_count = len(status["available_templates"])
        table.add_row("Templates", templates_status, f"Available: {templates_count}")
        
        write_status = "[CHECK] OK" if status["can_write"] else "[X] NO WRITE PERMISSION"
        table.add_row("Write Permission", write_status, status["current_directory"])
        
        table.add_row("Current Directory", "[INFO]", status["current_directory"])
        table.add_row("Output Path", "[INFO]", status["output_path"])
        table.add_row("Templates Path", "[INFO]", status["templates_absolute_path"])
        
        console.print(table)
        
        if status["available_templates"]:
            rprint(f"\n[cyan]Templates disponibles:[/cyan]")
            for template in status["available_templates"]:
                rprint(f"  • {template}")
        
        if not status["config_valid"]:
            rprint(f"\n[yellow]Para configurar API keys:[/yellow]")
            rprint(f"  export OPENAI_API_KEY=your_key")
            rprint(f"  export CLAUDE_API_KEY=your_key")
            rprint(f"  export DEEPSEEK_API_KEY=your_key")
            
    except Exception as e:
        rprint(f"[red]ERROR en doctor: {e}[/red]")
        import traceback
        rprint(f"[red]Traceback: {traceback.format_exc()}[/red]")

@app.command()
def version():
    """Mostrar version"""
    from . import __version__
    rprint(f"[cyan]Fast-Engine v{__version__}[/cyan]")
    rprint("[dim]Generador rapido de proyectos full-stack[/dim]")

@app.command("list-templates")
def list_templates():
    """Listar templates disponibles"""
    try:
        templates_dir = get_templates_dir()
        available = [p.name for p in templates_dir.iterdir() if p.is_dir()]

        if not available:
            rprint("[yellow]No hay templates disponibles[/yellow]")
            return

        table = Table(title="Templates Disponibles")
        table.add_column("Nombre", style="cyan")

        for t in available:
            table.add_row(t)

        console.print(table)

    except Exception as e:
        rprint(f"[red]ERROR: {e}[/red]")

@app.command()
def config(
    show: bool = typer.Option(False, "--show", help="Mostrar configuracion actual"),
    init: bool = typer.Option(False, "--init", help="Inicializar configuracion")
):
    """Gestionar configuracion"""
    try:
        if init:
            engine = FastEngine()
            engine.config.save()
            rprint("[green]Configuracion inicializada en fast-engine.json[/green]")
        elif show:
            engine = FastEngine()
            config_dict = {
                "openai_api_key": engine.config.openai_api_key or "Not set",
                "claude_api_key": engine.config.claude_api_key or "Not set",
                "deepseek_api_key": engine.config.deepseek_api_key or "Not set",
                "templates_path": engine.config.templates_path,
                "output_path": engine.config.output_path
            }
            
            rprint("[cyan]Configuracion actual:[/cyan]")
            for key, value in config_dict.items():
                if "api_key" in key and value != "Not set":
                    value = value[:8] + "..." if len(value) > 8 else value
                rprint(f"  {key}: {value}")
        else:
            rprint("[yellow]Usa --show para mostrar configuracion o --init para inicializar[/yellow]")
            
    except Exception as e:
        rprint(f"[red]ERROR: {e}[/red]")

if __name__ == "__main__":
    app()
