import cli
from backup.backups.cache import cache

from sysetup.models import Path
from sysetup.utils import download_directory


def setup() -> None:
    directories = (
        Path.assets,
        Path.HOME / ".local" / "share" / "kwalletd",
        Path.assets.parent / "backup",
    )
    for directory in directories:
        download_directory(directory)
    move_crontab()
    move_setup_files()


def move_crontab() -> None:
    src = Path.assets / "crontab" / "crontab"
    cli.run("crontab -", input=src.text)


def move_setup_files() -> None:
    setup_files_root = Path.assets / "files"
    setup_files = []
    archived_setup_files = []
    for path in setup_files_root.rglob("*"):
        if path.is_file():
            if path.archive_format is None:
                setup_files.append(path)
            else:
                archived_setup_files.append(path)

    if setup_files:
        cache.Backup(paths=setup_files).pull()

    source = cache.Backup().source
    for path in archived_setup_files:
        dest = (source / path.relative_to(setup_files_root)).parent
        if dest.is_root and not dest.exists():
            cli.run("mkdir -p", dest, root=True)
        else:
            dest.create_parent()
        with cli.status(f"Unpacking {path.relative_to(setup_files_root)}"):
            cli.capture_output("unzip -o", path, "-d", dest, root=dest.is_root)
