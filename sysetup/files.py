import cli

from backup.backup import Backup
from backup.backupmanager import BackupManager

from .path import Path


def setup():
    Backup().download("- /.config/browser/*", "+ /.config/scripts/backup/exports/.*", "- /.config/scripts/backup/exports/*", "/.**", quiet=False)
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
                [f'unzip -o "{src}" -d "{dst.parent}"']
                if src.suffix == ".zip"
                else [f"mkdir -p '{dst.parent}'", f"cp -f '{src}' '{dst}'"]
                )
            
            cli.get(*commands, root=dst.is_root)


def move_crontab():
    src = Path.assets / "crontab" / "crontab"
    cli.run(f"cat {src} | crontab -")
    

def trust_keyboard():
    keyboard = cli.get("bluetoothctl list | grep Keyboard")
    cli.run(f'bluetoothctl trust "{keyboard}"', wait=False) # blocks if not found


if __name__ == "__main__":
    setup()
