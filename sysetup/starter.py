import os

from libs.cli import Cli
from libs.gui import Gui

from backup import configure

from . import installer, git, desktopfiles, files


def setup():
    if "pw" not in os.environ:
        configure.start() # download core config files
        Cli.run("source ~/.bash_profile; sysetup")
    else:
        # core config files are available
        installer.install()
        git.setup()
        files.setup()
        #desktopfiles.setup()

        if Gui.ask_yn("Ready for reboot?"):
            Cli.run("sudo reboot now")

if __name__ == "__main__":
    setup()
