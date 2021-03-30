import os
import platform
from importlib import metadata

__all__ = ("name", "version", "node", "environment")

name = __package__
version = metadata.version(__package__)
node = platform.node()
environment = os.environ.get("APP_ENVIRONMENT", "dev")
