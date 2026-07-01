import os

import cli
from backup.syncer.builder import create_syncer
from superpathlib import Path

from sysetup.context import context, is_installed, is_linux

from .bitwarden import bitwarden_client


def download_directory(directory: Path) -> None:
    provision_rclone()
    create_syncer(directory=directory).capture_pull()


def provision_rclone() -> None:
    if not is_installed("rclone"):
        install_rclone()
    if "RCLONE_CONFIG_PASS" not in os.environ:
        os.environ["RCLONE_CONFIG_PASS"] = bitwarden_client().fetch_secret("rclone")
    config_file = Path.HOME / ".config" / "rclone" / "rclone.conf"
    if not config_file.exists():
        config_file.text = bitwarden_client().fetch_secret("rclone_conf")


def install_rclone() -> None:
    if is_linux():
        cli.run(context.package_install_command, "curl", root=True, check=False)
    command = "curl https://rclone.org/install.sh | sudo bash"
    cli.run_commands_in_shell(command, check=False)
