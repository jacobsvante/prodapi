from typing import Optional

from pydantic import BaseModel

from .. import info

__all__ = ("ServiceStatus",)


class ServiceStatus(BaseModel):
    ok: bool
    environment: str
    version: str
    node: str
    message: Optional[str] = None

    @classmethod
    def make(cls, *, ok: bool, message: str = None) -> "ServiceStatus":
        return cls(
            ok=ok,
            environment=info.environment,
            version=info.version,
            node=info.node,
            message=message,
        )
