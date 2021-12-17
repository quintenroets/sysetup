import os

from libs.cli import Cli
from libs.gui import Gui

from . import environment, installer, git, desktopfiles, files, constants


def setup():
    environment.setup()
    files.setup()
    desktopfiles.setup()
    installer.install()
    git.setup()

    if Gui.ask_yn("Ready for reboot?"):
        Cli.run("sudo reboot now")

if __name__ == "__main__":
    setup()
