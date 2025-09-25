import os

import cli
from backup.context import context as backup_context
from backup.syncer import Syncer
from backup.syncer.sync_configs import select_sync_config

from sysetup.models import Path

from .bitwarden import bitwarden


def download_directory(path: Path) -> None:
    download_item(directory=path)


def download_file(path: Path) -> None:
    download_item(path)


def download_item(path: Path | None = None, directory: Path | None = None) -> None:
    check_authenticated()
    location = path or directory
    assert location is not None
    config = select_sync_config(location)
    config.path = path
    config.directory = directory
    Syncer(config).capture_pull()


def check_authenticated() -> None:
    try:
        assert backup_context.secrets.rclone
    except cli.models.CalledProcessError:
        os.environ["RCLONE"] = "dummy"
        backup_context.secrets.rclone = bitwarden.client.fetch_secret("Rclone")
