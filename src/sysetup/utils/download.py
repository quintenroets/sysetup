import os

import cli
from backup.backups import Backup
from backup.context import context as backup_context
from backup.models import Path as BackupPath

from sysetup.models import Path

from .bitwarden import bitwarden


def download_directory(path: Path) -> None:
    check_authenticated()
    Backup(sub_check_path=BackupPath(path), confirm=False).pull()


def download_file(path: Path) -> None:
    check_authenticated()
    Backup(path=BackupPath(path), confirm=False).pull()


def check_authenticated() -> None:
    try:
        assert backup_context.secrets.rclone
    except cli.models.CalledProcessError:
        os.environ["RCLONE"] = "dummy"
        backup_context.secrets.rclone = bitwarden.client.fetch_secret("Rclone")
