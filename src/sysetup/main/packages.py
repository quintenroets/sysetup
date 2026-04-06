import shlex
from collections.abc import Iterable

import cli

from sysetup.context import context
from sysetup.context.system import is_linux
from sysetup.models import Path
from sysetup.utils import download_directory


def install_packages() -> None:
    download_directory(Path.packages)
    installations = (
        {"packages": None, "snap": "snap install"}
        if is_linux()
        else {"brew": "brew install"}
    )
    for name, command in installations.items():
        path = (Path.packages / name).with_suffix(".yaml")
        packages: list[str] = path.yaml
        install(packages, install_command=command)
    if is_linux() and not context.apt_is_installed:
        commands = "sudo pacman -S --noconfirm base-devel", "uv pip install wheel"
        cli.run_commands(*commands)


def install(packages: Iterable[str], install_command: str | None = None) -> None:
    if install_command is None:
        install_command = (
            "apt-get install -y"
            if context.apt_is_installed
            else "pacman -S --noconfirm"
        )
    for package in packages:
        args = shlex.split(package)
        cli.run(install_command, *args, root=is_linux(), check=False)
