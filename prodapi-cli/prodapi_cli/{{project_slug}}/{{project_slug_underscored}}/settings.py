from functools import lru_cache
from typing import List, Optional

from fastapi_security import HTTPBasicCredentials, PermissionOverrides
from pydantic import BaseSettings

__all__ = ("get_settings",)


class _Settings(BaseSettings):
    # NOTE: To set up OAuth2, you only need to supply
    #       `oidc_discovery_url` (preferred) OR `oauth2_jwks_url`
    oidc_discovery_url: Optional[str] = None
    oauth2_audiences: Optional[List[str]] = None
    basic_auth_credentials: Optional[List[HTTPBasicCredentials]] = None
    permission_overrides: PermissionOverrides = {}


@lru_cache()
def get_settings() -> _Settings:
    return _Settings()  # Reads variables from environment
