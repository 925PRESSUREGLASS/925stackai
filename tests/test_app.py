from typer.testing import CliRunner

from app import app


def test_placeholder() -> None:
    result = CliRunner().invoke(app, ["run"])
    assert "placeholder" in result.stdout.lower()
