from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import tomlkit
from pydantic import BaseModel, EmailStr, HttpUrl, conint, constr, validator

from . import constants, utils


class NewProjectSettingsIn(BaseModel):
    """All configuration related to setting up a new project"""

    project_name: constr(min_length=1)
    path: Path
    email: Optional[EmailStr]
    full_name: Optional[constr(min_length=1)]
    project_slug: Optional[constr(regex=constants.PROJECT_SLUG_REGEX)]
    project_short_description: Optional[str]
    dev_port: conint(ge=0, le=65535) = 8000
    github_username: Optional[constr(min_length=1)]
    github_repo_url: Optional[HttpUrl]
    documentation_url: Optional[HttpUrl]
    docker_image_repo_url: Optional[HttpUrl]
    basic_auth_credentials: Optional[List[Dict[str, str]]]
    oidc_discovery_url: Optional[HttpUrl]
    oauth2_audiences: Optional[List[str]]
    permission_overrides: Optional[Dict[str, str]]

    @validator("project_slug", always=True)
    def ensure_project_slug(cls, v, values):
        return v if v else utils.slugify(values["project_name"])

    @validator("github_repo_url", always=True)
    def ensure_github_repo_url(cls, v, values):
        username = values["github_username"]
        if username and not v:
            return f"https://github.com/{username}"
        else:
            return v

    @validator("documentation_url", always=True)
    def ensure_documentation_url(cls, v, values):
        return v or values["github_repo_url"]

    def finalize(self) -> "NewProjectSettings":
        out = self.copy(deep=True)
        if not out.project_slug:
            out.project_slug = utils.slugify(out.project_name)
        if not out.project_short_description:
            out.project_short_description = ""
        return NewProjectSettings(
            **out.dict(),
            project_slug_underscored=out.project_slug.replace("-", "_"),
        )


class NewProjectSettings(BaseModel):
    project_name: constr(min_length=1)
    path: Path
    email: Optional[EmailStr]
    full_name: Optional[constr(min_length=1)]
    project_slug: constr(regex=constants.PROJECT_SLUG_REGEX)
    project_slug_underscored: constr(min_length=1)
    project_short_description: str
    dev_port: conint(ge=0, le=65535)
    github_username: Optional[constr(min_length=1)]
    github_repo_url: Optional[HttpUrl]
    documentation_url: Optional[HttpUrl]
    docker_image_repo_url: Optional[HttpUrl]
    basic_auth_credentials: Optional[List[Dict[str, str]]]
    oidc_discovery_url: Optional[HttpUrl]
    oauth2_audiences: Optional[List[str]]
    permission_overrides: Optional[Dict[str, str]]
    project_slug: constr(regex=constants.PROJECT_SLUG_REGEX)
    project_short_description: str

    def to_toml(self) -> str:
        s = {k: utils.to_toml_value(v) for k, v in self.dict().items() if v is not None}
        return tomlkit.dumps(s)

    def to_template_variables(self) -> Dict[str, Any]:
        dct = self.dict()
        dct["settings"] = self
        dct["today"] = datetime.utcnow()
        return dct
