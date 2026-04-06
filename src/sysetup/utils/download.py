import os

from backup.syncer.builder import create_syncer

from sysetup.models import Path

from .bitwarden import bitwarden_client


def ensure_downloaded(path: Path) -> None:
    if not path.exists():
        download_directory(path.parent)


def download_directory(directory: Path) -> None:
    if "RCLONE" not in os.environ:
        os.environ["RCLONE"] = bitwarden_client().fetch_secret("Rclone")
    create_syncer(directory=directory).capture_pull()
