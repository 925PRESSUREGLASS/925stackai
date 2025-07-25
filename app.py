import typer
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

app = typer.Typer(help="Modular AI Agent CLI")

@app.callback()
def main() -> None:
    """Modular AI Agent CLI."""
    pass

@app.command()
def run():
    """Placeholder until agent is built."""
    typer.echo("Agent placeholder")

if __name__ == "__main__":
    app()
