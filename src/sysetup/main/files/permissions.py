import stat

import cli

from sysetup.models import Path
from sysetup.utils import download_directory


def setup() -> None:
    set_git_permissions()
    set_ssh_permissions()


def set_git_permissions() -> None:
    git_hooks_folder = Path.HOME / ".config" / "git" / "hooks"
    download_directory(git_hooks_folder)
    for path in git_hooks_folder.iterdir():
        cli.run("chmod +x", path)


def set_ssh_permissions() -> None:
    directory = Path.HOME / ".ssh"
    download_directory(directory)
    for path in directory.glob("id_*"):
        if path.suffix != ".pub":
            check_permissions(path)


def check_permissions(path: Path) -> None:
    permissions = path.stat().st_mode
    other_users_can_read = permissions & (stat.S_IRGRP | stat.S_IROTH)
    if other_users_can_read:
        path.chmod(33152)
