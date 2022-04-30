import cli
from backup.backup import Backup
from backup.backupmanager import BackupManager
from backup.path import Path as BackupPath

from .path import Path


def setup():
    exports_path = BackupPath.exports.relative_to(Path.HOME)
    script_assets = Path.script_assets.relative_to(Path.HOME)
    Backup().download(
        "- /.config/browser/*",
        "+ /{exports_path}/.*",
        "+ /{script_assets}/**",
        "- /{exports_path}/*",
        "/.**",
        quiet=False,
    )
    BackupManager.after_pull()

    move_files(Path.assets / "root")
    move_files(Path.assets / "home", Path.HOME)
    move_crontab()
    # trust_keyboard()
    # seems to work without this command for now


def move_files(src_root, dst_root=Path("/")):
    for src in src_root.rglob("*"):
        if src.is_file():
            dst = dst_root / src.relative_to(src_root)
            commands = (
                [f"unzip -o '{src}' -d '{dst.parent}'"]
                if src.suffix == ".zip"
                else [f"mkdir -p '{dst.parent}'", f"cp -f '{src}' '{dst}'"]
            )

            cli.run_commands(*commands, root=dst.is_root, capture_output=True)


def move_crontab():
    src = Path.assets / "crontab" / "crontab"
    cli.run("crontab -", input=src.text)


def trust_keyboard():
    keyboard = cli.get("bluetoothctl devices | grep Keyboard", shell=True)
    cli.run("bluetoothctl trust", keyboard, wait=False)  # blocks if not found


if __name__ == "__main__":
    setup()
