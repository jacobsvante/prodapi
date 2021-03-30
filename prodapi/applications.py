from typing import Iterable, List, Optional

from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from . import routes
from .sec import FastAPISecurity

__all__ = ("ProdAPI",)


class ProdAPI(FastAPI):
    def __init__(
        self,
        *,
        http_path_prefix: str = "",
        title: str = "ProdAPI",
        openapi_url: Optional[str] = "/openapi.json",
        docs_url: Optional[str] = "/docs",
        redoc_url: Optional[str] = "/redoc",
        **kw,
    ):
        if http_path_prefix.endswith("/"):
            raise RuntimeError("`http_path_prefix` must not end with a slash")

        super().__init__(
            title=title,
            openapi_url=self._prefixed_path(http_path_prefix, openapi_url),
            docs_url=self._prefixed_path(http_path_prefix, docs_url),
            redoc_url=self._prefixed_path(http_path_prefix, redoc_url),
            **kw,
        )
        self.http_path_prefix = http_path_prefix

    def include_router(self, router: APIRouter, **kw):
        prefix = kw.pop("prefix", "")
        super().include_router(
            router, prefix=self._prefixed_path(self.http_path_prefix, prefix), **kw
        )

    def with_health_routes(
        self,
        *,
        liveness_url: str = routes.health.DEFAULT_LIVENESS_URL,
        readiness_url: str = routes.health.DEFAULT_READINESS_URL,
        alive_checks: Iterable[routes.health.HealthCheckCallback] = (),
        ready_checks: Iterable[routes.health.HealthCheckCallback] = (),
        alive_tags: Optional[List[str]] = None,
        ready_tags: Optional[List[str]] = None,
    ) -> "ProdAPI":
        router = routes.health.make_router(
            liveness_url=liveness_url,
            readiness_url=readiness_url,
            alive_checks=alive_checks,
            ready_checks=ready_checks,
            alive_tags=alive_tags,
            ready_tags=ready_tags,
        )
        self.include_router(router)
        return self

    def with_user_routes(
        self, security: FastAPISecurity, *, user_details_url: str = "/users/me"
    ) -> "ProdAPI":
        self.include_router(
            routes.user.make_router(security, user_details_url=user_details_url)
        )
        return self

    def with_basic_cors(
        self, *, expose_headers: Optional[Iterable[str]] = None
    ) -> "ProdAPI":
        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=expose_headers,
        )
        return self

    @staticmethod
    def _prefixed_path(prefix, path) -> str:
        if not path.startswith("/"):
            path = f"/{path}"
        p = f"{prefix}{path}"
        if p.endswith("/"):
            p = p[0:-1]
        return p
