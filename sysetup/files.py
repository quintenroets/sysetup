from libs.cli import Cli

from .path import Path


def setup():    
    Cli.run(f"drive pull {path_name}" for path_name in ["", "browser"])
    move_files(Path.root / "root")
    move_files(Path.root / "home", Path.home)
    move_crontab()
    #Cli.run("bluetoothctl trust $(bluetoothctl list | grep Keyboard)", wait=False) # blocks if not found
    # seems to work without this command for now


def move_files(src_root, dst_root=Path("/")):
    for src in src_root.rglob("*"):
        if src.is_file():
            dst = dst_root / src.relative_to(src_root)
            if src.suffix == ".zip":
                commands = [
                    f'unzip -o "{src}" -d "{dst.parent}"'
                    ]
            else:
                commands = [
                    f"mkdir -p '{dst.parent}'",
                    f"cp -f '{src}' '{dst}'"
                    ]
            
            while not dst.exists():
                dst = dst.parent
            root = dst.stat().st_uid == 0
            if root:
                commands = [f"sudo {c}" for c in commands]
            Cli.get(commands)


def move_crontab():
    src = Path.root / "crontab" / "crontab"
    Cli.run(f"cat {src} | crontab -")


if __name__ == "__main__":
    setup()
