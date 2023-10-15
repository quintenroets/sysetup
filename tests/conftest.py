import pytest

from sysetup.path import Path


def provision_path():
    with Path.tempfile() as path:
        yield path
    assert not path.exists()


@pytest.fixture()
def path():
    yield from provision_path()
