import os

from libs.cli import Cli
from libs.gui import Gui

from backup.backup import Backup

from . import installer, git, desktopfiles, files


def setup():
    if "pw" not in os.environ:
        # download and apply core config files
        Backup.download(Path.home(), "Config", filters=["+ /.*"])
        Cli.run("source ~/.bash_profile; sysetup")

    else:
        # core config files are available
        files.setup() # files needed to know what to install
        installer.install()
        git.setup()
        #desktopfiles.setup()

        if Gui.ask_yn("Ready for reboot?"):
            Cli.run("sudo reboot now")

if __name__ == "__main__":
    setup()
