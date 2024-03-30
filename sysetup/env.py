import os

from backup.backups.remote import Backup

from .path import Path


def setup():
    if "SUDO_ASKPASS" not in os.environ:
        path = Path(".bash_profile")
        Backup(quiet=False, path=path).pull()
        raise NotImplementedError
        # TODO load environment


if __name__ == "__main__":
    setup()
