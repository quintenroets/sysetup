from backup.backups import Backup
from backup.models import Path as BackupPath

from sysetup.models import Path


def download_directory(path: Path) -> None:
    Backup(sub_check_path=BackupPath(path), confirm=False).pull()


def download_file(path: Path) -> None:
    Backup(path=BackupPath(path), confirm=False).pull()
