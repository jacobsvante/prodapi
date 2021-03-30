import re

from prodapi import __version__, info


def test_version():
    assert __version__ == info.version
    assert re.match(r"^\d+\.\d+\.\d+$", info.version)


def test_name():
    assert info.name == "prodapi"


def test_environment():
    assert info.environment == "dev"


def test_node():
    assert isinstance(info.node, str)
    assert len(info.node) > 0
