import cli

from sysetup.context import context
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

    nginx_path = Path("/") / "etc" / "nginx" / "sites-enabled" / "default"
    if nginx_path.exists():
        cli.run("rm", nginx_path, root=True)


def set_background() -> None:  # pragma: nocover
    wallpaper_path = (
        Path.HOME / ".local" / "share" / "wallpapers" / "Qwallpapers" / "background.jpg"
    )
    download_directory(wallpaper_path.parent)
    wallpaper_uri = wallpaper_path.as_uri()
    script = Path.update_wallpaper_script.text.replace(
        "__wallpaper_uri__",
        wallpaper_uri,
    )
    run_kde_script(script)


def run_kde_script(script: str) -> None:  # pragma: nocover
    command = (
        "qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript"
    )
    if not context.is_running_in_test and cli.completes_successfully("which qdbus"):
        cli.run(command, script)
