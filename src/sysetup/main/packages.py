import platform
import shlex
import warnings
from collections.abc import Iterable

import cli

from sysetup.context import context
from sysetup.models import Path
from sysetup.utils import bitwarden, download_directory, is_installed


def setup() -> None:
    enable_sudo()
    update_package_manager()
    install_packages()
    cleanup_after_install()


def enable_sudo() -> None:
    password = bitwarden.client.fetch_secret("Laptop")
    cli.run("sudo -S true", input=password)  # activate sudo without askpass


def install_packages() -> None:
    download_directory(Path.packages)
    installations = {"packages": None, "snap": "snap install"}
    for name, command in installations.items():
        path = (Path.packages / name).with_suffix(".yaml")
        packages: list[str] = path.yaml
        install(packages, install_command=command)

    if not context.apt_is_installed:
        commands = "sudo pacman -S --noconfirm base-devel", "uv pip install wheel"
        cli.run_commands(*commands)


def cleanup_after_install() -> None:
    if context.apt_is_installed:
        cli.run("sudo apt-get autoremove -y")
    cli.run("tlp start", root=True)
    if is_installed("qdbus"):
        commands = "rm /usr/bin/qdbus", "ln -s /usr/lib/qt6/bin/qdbus /usr/bin/qdbus"
        cli.run_commands(*commands, root=True)
    delete = "apt purge -y" if context.apt_is_installed else "pacman -R --noconfirm"
    commands = (
        "auto-cpufreq --install",  # Fails on VM
        f"{delete} firefox",  # fails if firefox not installed
    )
    cli.run_commands(*commands, check=False, root=True)


def update_package_manager() -> None:
    if context.apt_is_installed:
        update_apt()
    else:
        cli.run("pacman -Syy", root=True)


def update_apt() -> None:
    value = (
        "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true"
    )
    agree_eula_command = f'echo "{value}" | sudo debconf-set-selections'
    commands = "sudo apt-get update", agree_eula_command
    cli.run_commands_in_shell(*commands)
    if not Path("/snap").exists():
        cli.run("ln -s /var/lib/snapd/snap /snap", root=True)


def install(packages: Iterable[str], install_command: str | None = None) -> None:
    if install_command is None:
        install_command = (
            "apt-get install -y"
            if context.apt_is_installed
            else "pacman -S --noconfirm"
        )

    is_linux = platform.system() == "Linux"
    if not is_linux:
        message = "Required packages can only be installed on Linux"
        warnings.warn(message, stacklevel=2)
        return

    for package in packages:
        args = shlex.split(package)
        cli.run(install_command, *args, root=True, check=False)
