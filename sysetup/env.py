import os
from dotenv import load_dotenv

from backup.backup import Backup

from .path import Path


def setup():
    if "pw" not in os.environ:
        Backup().download("/.bash_profile", quiet=False)
        load_dotenv(dotenv_path=Path.HOME / ".bash_profile")


if __name__ == "__main__":
    setup()
