import typer
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from typing import Optional
from .core import FastEngine
import os

app = typer.Typer(help="Fast-Engine: Generador rapido de proyectos full-stack")
console = Console()

@app.command()
def init(
    name: str = typer.Argument(..., help="Nombre del proyecto"),
    template: str = typer.Option("saas-basic", "--template", "-t", help="Template a usar"),
    description: str = typer.Option("", "--description", "-d", help="Descripcion del proyecto")
):
    """Crear nuevo proyecto"""
    try:
        engine = FastEngine()
        result = engine.init_project_demo(name, template, description)
        rprint(f"[green]{result}[/green]")
        
        rprint("\n[bold cyan]EXITO! Proyecto creado exitosamente![/bold cyan]")
        rprint(f"\n[yellow]Siguientes pasos:[/yellow]")
        rprint(f"  cd {name}")
        rprint(f"  python main.py")
        rprint(f"  # o docker-compose up -d")
        
    except Exception as e:
        rprint(f"[red]ERROR: {e}[/red]")
        import traceback
        rprint(f"[red]Traceback: {traceback.format_exc()}[/red]")
        raise typer.Exit(1)

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

@app.command()
def templates():
    """Listar templates disponibles"""
    try:
        engine = FastEngine()
        available_templates = engine.template_engine.list_templates()
        
        if not available_templates:
            rprint("[yellow]No hay templates disponibles[/yellow]")
            rprint("[dim]Los templates se crearan automaticamente cuando los necesites[/dim]")
            return
        
        table = Table(title="Templates Disponibles")
        table.add_column("Nombre", style="cyan")
        table.add_column("Descripcion")
        
        for template_name in available_templates:
            try:
                config = engine.template_engine.load_template_config(template_name)
                description = config.get("description", "Sin descripcion")
                table.add_row(template_name, description)
            except Exception:
                table.add_row(template_name, "Error cargando configuracion")
        
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
