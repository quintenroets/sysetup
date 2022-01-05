import os

from libs import env

from backup.backup import Backup


def setup():
    if "pw" not in os.environ:
        Backup().download("/.bash_profile", quiet=False)
        env.load()


if __name__ == "__main__":
    setup()
