import os

from libs.cli import Cli
from libs.gui import Gui

from backup.backup import Backup

from . import installer, git, files


def setup():
    if "pw" in os.environ:
        setup_in_env()
    else:
        # download and load core config
        Backup.download(Path.home(), "Config", filters=["+ /.*"])
        Cli.run("source ~/.bash_profile", "sysetup")
    
def setup_in_env():
    files.setup() # files needed to know what to install
    installer.install()
    git.setup()

    if Gui.ask_yn("Ready for reboot?"):
        Cli.run("sudo reboot now")

if __name__ == "__main__":
    setup()
