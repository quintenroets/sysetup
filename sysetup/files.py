from pathlib import Path

from libs.cli import Cli

from .filemanager import FileManager

def setup():
    move_files(FileManager.root / "root")
    move_files(FileManager.root / "home", Path.home())
    #Cli.run("bluetoothctl trust $(bluetoothctl list | grep Keyboard)", wait=False) # blocks if not found
    # seems to work without this command for now


def move_files(src_root, dst_root=Path("/")):
    for src in src_root.rglob("*"):
        if src.is_file():
            dst = dst_root / src.relative_to(src_root)
            command = (
                f'sudo unzip -o "{src}" -d "{dst.parent}"'
                if src.suffix == ".zip"
                else f'sudo mkdir -p "{dst.parent}"; sudo cp -f "{src}" "{dst}"'
            )
            Cli.get(command)

if __name__ == "__main__":
    setup()
