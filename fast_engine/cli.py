"""CLI for fast-engine."""

import typer

app = typer.Typer(help="fast-engine command line interface")


@app.command()
def main():
    """Default command prints a greeting."""
    typer.echo("Welcome to fast-engine!")


if __name__ == "__main__":
    app()
