import os

from libs.cli import Cli
from libs.gui import Gui

from backup.backup import Backup

from . import installer, git, files


def setup():
    Cli.run(f"drive pull {path_name}" for path_name in ["config", "docs", "browser"])
    
    if "pw" in os.environ:
        setup_root()
    else:
        # load new environ
        Cli.run("source ~/.bash_profile", "sysetup")
    
def setup_root():
    files.setup() # files needed to know what to install
    installer.install()
    git.setup()

    if Gui.ask_yn("Ready for reboot?"):
        Cli.run("sudo reboot now")

if __name__ == "__main__":
    setup()
