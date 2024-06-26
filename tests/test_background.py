import os
from collections.abc import Callable, Iterator

import cli
import pytest
from backup.context import context
from backup.utils import setup
from sysetup.main.files import set_background
from sysetup.models import Path

plasma_config_path = Path.HOME / ".config" / "plasma-org.kde.plasma.desktop-appletsrc"


@pytest.fixture
def restore(path: Path) -> Callable[[Path], Iterator[None]]:
    def _restore(restored_path: Path) -> Iterator[None]:
        if restored_path.exists():
            restored_path.copy_to(path, include_properties=False)
        yield
        path.rename(restored_path, exist_ok=True)

    return _restore


@pytest.fixture
def restore_and_check(
    path: Path, restore: Callable[[Path], Iterator[None]]
) -> Callable[[Path], Iterator[None]]:
    setup.check_setup()
    env = os.environ | {"RCLONE_CONFIG_PASS": context.secrets.rclone}
    env.pop("RCLONE_PASSWORD_COMMAND", None)

    def _restore_and_check(restored_path: Path) -> Iterator[None]:
        content_hash = cli.capture_output("rclone hashsum MD5", restored_path, env=env)
        yield from restore(restored_path)
        assert (
            cli.capture_output("rclone hashsum MD5", restored_path, env=env)
            == content_hash
        )

    return _restore_and_check


@pytest.fixture
def restore_config_path(
    restore_and_check: Callable[[Path], Iterator[None]],
) -> Iterator[None]:
    yield from restore_and_check(plasma_config_path)


def test_wallpaper(restore_config_path: Callable[[Path], Iterator[None]]) -> None:
    set_background()
    assert "Qwallpapers" in plasma_config_path.text
