import cli
import pytest

from sysetup.files import set_background
from sysetup.path import Path

plasma_config_path = Path.HOME / ".config" / "plasma-org.kde.plasma.desktop-appletsrc"


@pytest.fixture
def restore(path: Path):
    def _restore(restored_path: Path):
        if restored_path.exists():
            restored_path.copy_to(path)
        yield
        path.rename(restored_path, exist_ok=True)

    return _restore


@pytest.fixture
def restore_and_check(path: Path, restore):
    def _restore_and_check(restored_path: Path):
        content_hash = cli.get("rclone hashsum MD5", restored_path)
        yield from restore(restored_path)
        assert cli.get("rclone hashsum MD5", restored_path) == content_hash

    return _restore_and_check


@pytest.fixture
def restore_config_path(restore_and_check):
    yield from restore_and_check(plasma_config_path)


def test_wallpaper(restore_config_path):
    set_background()
    assert "Qwallpapers" in plasma_config_path.text
