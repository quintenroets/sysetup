import os

import cli.env
from backup.backups.remote import Backup

from .path import Path


def setup():
    if "SUDO_ASKPASS" not in os.environ:
        path = Path(".bash_profile")
        Backup(quiet=False, path=path).pull()
        cli.env.load()


if __name__ == "__main__":
    setup()
