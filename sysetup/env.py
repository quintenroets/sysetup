import os

import cli.env
from backup.backups.remote import Backup

from .path import Path


def setup():
    if "pw" not in os.environ:
        paths = (Path(".bash_profile"),)
        Backup(quiet=False, paths=paths).pull()
        cli.env.load()


if __name__ == "__main__":
    setup()
