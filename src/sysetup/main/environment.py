import json
import os
from typing import cast

import cli
from dotenv import load_dotenv

from sysetup.context import context
from sysetup.models import Path
from sysetup.utils import download_file, is_installed

from .installations import enable_service
from .packages import update_package_manager


def setup() -> None:
    os.environ["GITHUB"] = fetch_secret("GitHub")
    os.environ["RCLONE"] = fetch_secret("Rclone")
    download_file(Path("etc") / "environment")
    if "SUDO_ASKPASS" not in os.environ:
        download_file(Path.profile)
        load_dotenv(dotenv_path=Path.profile)


def fetch_secret(name: str) -> str:
    if not is_installed("bw"):
        update_package_manager()
        command = (
            "apt-get install -y build-essential libdbus-glib-1-dev libgirepository1.0-dev "
            "preload pulseaudio tlp unattended-upgrades qtchooser"
        )
        cli.run(command, root=True)
        cli.run("sudo apt-get install -y snapd", root=True)
        # cli.run("/usr/lib/snapd/snapd", root=True)
        # cli.run("systemctl status snapd", root=True)
        cli.run("snap install bw", root=True)
    email = os.environ.get("EMAIL", "quinten.roets@gmail.com")
    if "BW_SESSION" not in os.environ:
        output = cli.capture_output(f"bw login {email} {context.options.password}")
        os.environ["BW_SESSION"] = output.split("--session ")[-1]
    response = cli.capture_output(f"bw list items --search {name}")
    secret = json.loads(response)[0]["notes"]
    return cast(str, secret)
