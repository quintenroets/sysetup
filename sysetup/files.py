import cli
from backup.backups import Backup
from backup.utils import Path as BackupPath

from .path import Path


def setup():
    sub_check_path = BackupPath.script_assets
    kwargs_mapper = {
        "Script assets": dict(sub_check_path=sub_check_path),
        "environment": dict(
            filter_rules=["+ /etc/environment", "- *"], sync_remote=False
        ),
    }
    for name, kwargs in kwargs_mapper.items():
        print(f"Downloading {name}..")
        Backup(quiet=False, confirm=False, **kwargs).pull()

    move_crontab()
    # trust_keyboard()
    # seems to work without this command for now


def move_crontab():
    src = Path.assets / "crontab" / "crontab"
    cli.run("crontab -", input=src.text)


def trust_keyboard():
    keyboard = cli.get("bluetoothctl devices | grep Keyboard", shell=True)
    cli.run("bluetoothctl trust", keyboard, wait=False)  # blocks if not found


if __name__ == "__main__":
    setup()
