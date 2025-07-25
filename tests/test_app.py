from typer.testing import CliRunner
from app import app

def test_placeholder():
    result = CliRunner().invoke(app, ["run"])
    assert "placeholder" in result.stdout.lower()
