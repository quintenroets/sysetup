import os

from libs.cli import Cli
from libs.gui import Gui

from . import environment, installer, git, desktopfiles, files


def setup():
    return
    environment.setup()
    installer.install()
    desktopfiles.setup()
    git.setup()
    files.setup()

    if Gui.ask_yn("Ready for reboot?"):
        Cli.run("sudo reboot now")

if __name__ == "__main__":
    setup()
