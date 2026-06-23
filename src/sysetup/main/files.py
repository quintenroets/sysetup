import stat

import cli

from sysetup.context.system import is_linux
from sysetup.models import Path
from sysetup.utils import download_directory


def setup() -> None:
    configure_git()
    configure_ssh()
    remove_clutter()


def configure_git() -> None:
    directory = Path.HOME / ".config" / "git" / "hooks"
    download_directory(directory)
    for path in directory.iterdir():
        cli.run("chmod +x", path)


def configure_ssh() -> None:
    directory = Path.HOME / ".ssh"
    download_directory(directory)
    if is_linux():
        remove_macos_ssh_options(directory / "config")
    for path in directory.glob("id_*"):
        if path.suffix != ".pub":
            check_permissions(path)


def remove_macos_ssh_options(config: Path) -> None:
    lines = (line for line in config.lines if "UseKeychain" not in line)
    config.lines = list(lines)


def check_permissions(path: Path) -> None:
    permissions = path.stat().st_mode
    other_users_can_read = permissions & (stat.S_IRGRP | stat.S_IROTH)
    if other_users_can_read:
        path.chmod(0o600)


def remove_clutter() -> None:
    names = (
        "Desktop",
        "Downloads",
        "Music",
        "Pictures",
        "Public",
        "Templates",
        "Videos",
    )
    for name in names:
        path = Path.HOME / name
        path.rmtree(missing_ok=True)

    root = Path("/") if is_linux() else Path("/") / "opt" / "homebrew"
    nginx_path = root / "etc" / "nginx" / "sites-enabled" / "default"
    if nginx_path.exists():
        cli.run("rm", nginx_path, root=True)
