import os

from libs.cli import Cli
from libs.gui import Gui

from backup import configure

from . import environment, installer, git, desktopfiles, files


def setup():

    if "pw" not in os.environ:
        print("NOT AVAILABLE")
        configure.start()
        Cli.run("sysetup")
    else:
        print("GELUKT")
    return
    environment.setup()
    return
    installer.install()
    desktopfiles.setup()
    git.setup()
    files.setup()

    if Gui.ask_yn("Ready for reboot?"):
        Cli.run("sudo reboot now")

if __name__ == "__main__":
    setup()
