import cli
from backup.backups import Backup
from backup.backups.cache import raw
from backup.utils import Path as BackupPath

from .path import Path


def setup():
    kwargs_mapper = {
        "Script assets": dict(sub_check_path=BackupPath.script_assets),
        "environment": dict(
            sub_check_path=Path("/") / "etc", filter_rules=["+ /environment", "- *"]
        ),
        "setup files": dict(
            sub_check_path=BackupPath.script_assets / "sysetup" / "files"
        ),
    }
    for name, kwargs in kwargs_mapper.items():
        print(f"Downloading {name}..")
        Backup(quiet=False, confirm=False, **kwargs).pull()

    move_crontab()
    move_setup_files()


def move_crontab():
    src = Path.assets / "crontab" / "crontab"
    cli.run("crontab -", input=src.text)


def move_setup_files():
    setup_files_root = BackupPath.script_assets / "sysetup" / "files"
    setup_files = []
    archived_setup_files = []
    for path in setup_files_root.rglob("*"):
        if path.is_file():
            files = setup_files if path.archive_format is None else archived_setup_files
            files.append(path)

    backup = raw.Backup(paths=setup_files)
    backup.pull()

    for path in archived_setup_files:
        dest = (backup.source / path.relative_to(setup_files_root)).parent
        with cli.status(f"Unpacking {path.relative_to(setup_files_root)}"):
            cli.get("unzip -o", path, "-d", dest, root=dest.is_root)


if __name__ == "__main__":
    setup()
