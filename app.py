import argparse
import sys
import typer
from dotenv import load_dotenv

load_dotenv()

app = typer.Typer(help="Modular AI Agent CLI")


@app.callback()
def main() -> None:
    """Modular AI Agent CLI."""
    pass


@app.command()
def run() -> None:
    """Placeholder until agent is built."""
    typer.echo("Agent placeholder")


def cli() -> None:
    """CLI entrypoint wrapping the Typer application."""
    parser = argparse.ArgumentParser(description="Modular AI Agent")
    parser.add_argument("args", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    sys.argv = [sys.argv[0]] + args.args
    app()


if __name__ == "__main__":
    cli()

