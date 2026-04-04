import os

import cli
from backup.context import context as backup_context
from backup.syncer.builder import create_syncer

from sysetup.models import Path

from .bitwarden import bitwarden_client


def download_directory(path: Path) -> None:
    check_authenticated()
    create_syncer(directory=path).capture_pull()


def check_authenticated() -> None:
    try:
        _ = backup_context.secrets.rclone
    except cli.models.CalledProcessError:
        os.environ["RCLONE"] = "dummy"
        backup_context.secrets.rclone = bitwarden_client().fetch_secret("Rclone")
