import logging
from pathlib import Path
from typing import Any, Dict, Iterable

import jinja2

from .settings import NewProjectSettings

__all__ = ("new_project",)

logger = logging.getLogger(__name__)


jinja_env = jinja2.Environment(
    loader=jinja2.PackageLoader("prodapi_cli", package_path="."),
    undefined=jinja2.StrictUndefined,
    keep_trailing_newline=True,
)


def new_project(settings: NewProjectSettings):
    template_paths = jinja_env.list_templates(
        filter_func=_ignore_template_files_callback
    )
    logger.debug(f"Found templates: {template_paths}")

    variables = settings.to_template_variables()
    logger.debug(f"Template variables: {variables}")

    path_to_rendered = render_templates(template_paths, variables)

    for path, rendered in path_to_rendered.items():
        num_chars = len(rendered)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered)
        logger.debug(f"Dumped {path} to file system ({num_chars} chars)")


def render_templates(
    template_paths: Iterable[str], variables: Dict[str, Any]
) -> Dict[Path, str]:
    path_to_rendered = {}
    for template_path in template_paths:
        output_path = Path(jinja_env.from_string(template_path).render(**variables))

        logger.info(f"Generating file {output_path}")
        template = jinja_env.get_template(template_path)
        rendered = template.render(**variables)
        logger.debug(f"{rendered}\n\n")
        path_to_rendered[output_path] = rendered

    return path_to_rendered


def _ignore_template_files_callback(template_name: str) -> bool:
    return template_name.startswith("{{project_slug}}") and not template_name.endswith(
        (".pyc", ".DS_Store")
    )
