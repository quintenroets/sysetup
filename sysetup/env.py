import cli.env
import os

from backup.backup import Backup


def setup():
    if "pw" not in os.environ:
        Backup().download("/.bash_profile", quiet=False)
        cli.env.load()


if __name__ == "__main__":
    setup()
