import enum
import logging
from pathlib import Path
from typing import Optional

import typer
from typer import Argument, Option

from . import generator, info
from .settings import NewProjectSettingsIn

# from uuid import UUID
# from typing import Optional


__all__ = ("app",)

app = typer.Typer()
# app.add_typer(manifests.app, name="manifests")

state = {"config_path": None}


class LogLevel(str, enum.Enum):
    debug = "debug"
    info = "info"
    warning = "warning"
    error = "error"
    critical = "critical"

    def to_native(self) -> int:
        return getattr(logging, self.value.upper())


@app.callback()
def main(
    config_path: Optional[Path] = Option(None),
    log_level: LogLevel = Option(LogLevel.warning, "-l", "--log-level"),
):
    """ProdAPI command line utilities"""
    logging.basicConfig(level=log_level.to_native())
    app_dir = Path(typer.get_app_dir("prodapi"))
    app_dir.mkdir(parents=True, exist_ok=True)

    if not config_path:
        config_path = Path(app_dir) / "config.yaml"
    state["config_path"] = config_path

    if config_path.is_file():
        typer.secho("Loaded config: {config_path}", err=True)


@app.command()
def global_config_path():
    """Print where the config is searched for and exit"""
    typer.echo(state["config_path"])


@app.command()
def version():
    """Print the prodapi-cli version"""
    typer.echo(f"prodapi-cli: {info.version}")


@app.command()
def new(
    project_name: str = Argument(...),
    dry_run: bool = Option(
        False,
        help="Don't actually create anything, just print what would happen when running without this flag",
    ),
):
    """✨ Create a new prodapi project ✨"""
    if dry_run:
        typer.secho("[Dry run] Not actually creating anything...", fg="magenta")
    path = (Path(".") / project_name).absolute()

    if path.exists():
        typer.secho(f"Path {path} already exists", fg="red")
        raise typer.Abort()

    typer.secho(f"Creating prodapi app {project_name} @ {path}", fg="blue")

    settings = NewProjectSettingsIn(project_name=project_name, path=path)
    settings = settings.finalize()
    generator.new_project(settings)

    typer.secho(f"Created app {project_name}!", fg="green")

    # raise NotImplementedError("Continue creating this!")
