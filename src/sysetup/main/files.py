import stat

import cli

from sysetup.context import context
from sysetup.context.system import is_installed, is_linux
from sysetup.models import Path
from sysetup.utils import download_directory


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


def set_background() -> None:  # pragma: nocover
    wallpaper_path = (
        Path.HOME / ".local" / "share" / "wallpapers" / "Qwallpapers" / "background.jpg"
    )
    download_directory(wallpaper_path.parent)
    script = Path.update_wallpaper_script.text
    script = script.replace("__wallpaper_uri__", wallpaper_path.as_uri())
    run_kde_script(script)


def run_kde_script(script: str) -> None:  # pragma: nocover
    command = (
        "qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript"
    )
    if not context.is_running_in_test and is_installed("qdbus"):
        cli.run(command, script)


def install_crontab() -> None:
    src = Path.assets / "crontab" / "crontab"
    cli.run("crontab -", input=src.text)


def configure_git() -> None:
    directory = Path.HOME / ".config" / "git" / "hooks"
    download_directory(directory)
    for path in directory.iterdir():
        cli.run("chmod +x", path)


def configure_ssh() -> None:
    directory = Path.HOME / ".ssh"
    download_directory(directory)
    for path in directory.glob("id_*"):
        if path.suffix != ".pub":
            check_permissions(path)


def check_permissions(path: Path) -> None:
    permissions = path.stat().st_mode
    other_users_can_read = permissions & (stat.S_IRGRP | stat.S_IROTH)
    if other_users_can_read:
        path.chmod(0o600)
