import os
import platform

try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata  # Python 3.7 and lower

__all__ = ("name", "version", "node", "environment")

name = __package__
version = metadata.version(__package__)
node = platform.node()
environment = os.environ.get("APP_ENVIRONMENT", "dev")
