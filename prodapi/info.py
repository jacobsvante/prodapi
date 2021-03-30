import os
import platform

try:
    from importlib import metadata
except ImportError:
    # Python 3.7 and lower
    import importlib_metadata as metadata  # type: ignore

__all__ = ("name", "version", "node", "environment")

name = __package__
version = metadata.version(__package__)
node = platform.node()
environment = os.environ.get("APP_ENVIRONMENT", "dev")
