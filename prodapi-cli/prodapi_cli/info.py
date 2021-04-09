try:
    from importlib.metadata import version as _version_func  # type: ignore
except ImportError:
    # Python 3.7 and lower
    from importlib_metadata import version as _version_func  # type: ignore


version = _version_func(__package__)
