import shutil

from libs.cli import Cli
from libs.gui import Gui
from libs import folders

from .filemanager import FileManager

def setup():
    Cli.run("drive pull", "drive pull browser", "drive pull config")

    # apply new config files
    Cli.run(f"source ~/bash_profile")

    sleep_command = f"""#!/bin/bash
case "$1" in
    post)
        sh {folders.scripts / "system" / "system" / "aftersleep"}
    ;;
esac"""
    sleep_path = "/usr/lib/systemd/system-sleep/custom"
    FileManager.save(sleep_command, sleep_path)

    assets = FileManager.root

    Cli.run(
        f"sudo chmod +x {sleep_path}",

        f"unzip -o {assets}/plasma/Win11.zip -d $HOME/.local/share/icons",
        f"sudo unzip -o {assets}/plasma/sugar-candy.zip -d /usr/share/sddm/themes",
        "sudo mkdir -p /etc/sddm.conf",
        f"sudo cp -f {assets}/plasma/kde_settings.conf /etc/sddm.conf/kde_settings.conf",

        "bluetoothctl trust 70:99:1C:8A:2A:FE"
    )

if __name__ == "__main__":
    setup()
