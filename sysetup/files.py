import cli
from backup.backups import backup

from .path import Path


def setup():
    kwargs_list = [
        dict(folder=Path.script_assets),
        dict(filter_rules=[f"- {Path.HOME}/**"]),  # need /etc/environment
    ]
    for kwargs in kwargs_list:
        backup.Backup(quiet=False, confirm=False, **kwargs).pull()

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
