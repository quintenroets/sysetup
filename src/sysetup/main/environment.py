import os

from backup.backups.remote import Backup
from backup.models import Path
from dotenv import load_dotenv


def setup() -> None:
    if "SUDO_ASKPASS" not in os.environ:
        path = Path(".bash_profile")
        Backup(path=path).pull()
        load_dotenv(dotenv_path=Path.HOME / path)
