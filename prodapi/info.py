import os
import platform

try:
    from importlib.metadata import version as _version_func  # type: ignore
except ImportError:
    # Python 3.7 and lower
    from importlib_metadata import version as _version_func  # type: ignore

__all__ = ("name", "version", "node", "environment")

name = __package__
version = _version_func(__package__)
node = platform.node()
environment = os.environ.get("APP_ENVIRONMENT", "dev")
