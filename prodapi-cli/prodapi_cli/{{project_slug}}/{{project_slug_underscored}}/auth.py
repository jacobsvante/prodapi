from prodapi import FastAPISecurity

from .settings import get_settings

__all__ = ("security",)


settings = get_settings()
security = FastAPISecurity()

if settings.basic_auth_credentials:
    security.init_basic_auth(settings.basic_auth_credentials)

if settings.oidc_discovery_url:
    security.init_oauth2_through_oidc(
        settings.oidc_discovery_url,
        audiences=settings.oauth2_audiences,
    )

security.add_permission_overrides(settings.permission_overrides or {})
