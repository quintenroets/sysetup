import cli

from sysetup.context import context
from sysetup.context.system import is_installed
from sysetup.models import Path
from sysetup.utils import ensure_downloaded

from . import installations, packages


def setup() -> None:
    set_background()
    packages.setup()
    install_crontab()
    installations.setup()


def set_background() -> None:  # pragma: nocover
    path = (
        Path.HOME / ".local" / "share" / "wallpapers" / "Qwallpapers" / "background.jpg"
    )
    ensure_downloaded(path)
    script = Path.update_wallpaper_script.text
    script = script.replace("__wallpaper_uri__", path.as_uri())
    command = (
        "qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript"
    )
    if not context.is_running_in_test and is_installed("qdbus"):
        cli.run(command, script)


def install_crontab() -> None:
    path = Path.assets / "crontab" / "crontab"
    ensure_downloaded(path)
    cli.run("crontab -", input=path.text)
