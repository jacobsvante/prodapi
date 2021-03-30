from typing import Callable, Iterable, List, Optional

from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from ..models import ServiceStatus

__all__ = ("make_router",)

DEFAULT_LIVENESS_URL = "/__is-alive"
DEFAULT_READINESS_URL = "/__is-ready"

HealthCheckCallback = Callable[[], Optional[str]]


def make_router(
    *,
    liveness_url: str,
    readiness_url: str,
    alive_checks: Iterable[HealthCheckCallback] = (),
    ready_checks: Iterable[HealthCheckCallback] = (),
    alive_tags: Optional[List[str]] = None,
    ready_tags: Optional[List[str]] = None,
) -> APIRouter:
    router = APIRouter()

    @router.get(
        liveness_url,
        response_model=ServiceStatus,
        responses={503: {"model": ServiceStatus}},
        summary="Check if app responds",
        tags=alive_tags or ["Health"],
    )
    async def health_is_alive():
        return _make_service_status(alive_checks)

    @router.get(
        readiness_url,
        response_model=ServiceStatus,
        responses={503: {"model": ServiceStatus}},
        summary="Check if app is ready to serve requests",
        tags=ready_tags or ["Health"],
    )
    async def health_is_ready():
        return _make_service_status(ready_checks)

    return router


def _make_service_status(
    health_checks: Iterable[HealthCheckCallback],
) -> ORJSONResponse:
    for check in health_checks:
        failure_message = check()
        if failure_message:
            s = ServiceStatus.make(ok=False, message=failure_message)
            return ORJSONResponse(content=s.dict(), status_code=503)

    return ORJSONResponse(content=ServiceStatus.make(ok=True).dict(), status_code=200)
