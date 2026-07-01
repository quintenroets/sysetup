import shlex
from collections.abc import Iterable

import cli
from superpathlib import Path

from sysetup.context import context, is_linux

from .download import download_directory


def install_packages() -> None:
    directory = Path.script_assets / Path(__file__).parent.parent.name / "packages"
    download_directory(directory)
    installations = (
        {"packages": None, "snap": "snap install"}
        if is_linux()
        else {"brew": "brew install"}
    )
    for name, command in installations.items():
        path = (directory / name).with_suffix(".yaml")
        packages: list[str] = path.yaml
        install(packages, install_command=command)
    if is_linux() and not context.apt_is_installed:
        commands = "sudo pacman -S --noconfirm base-devel", "uv pip install wheel"
        cli.run_commands(*commands)


def install(packages: Iterable[str], install_command: str | None = None) -> None:
    if install_command is None:
        install_command = context.package_install_command
    for package in packages:
        args = shlex.split(package)
        cli.run(install_command, *args, root=is_linux(), check=False)
