import cli

from sysetup.context import context
from sysetup.models import Path
from sysetup.utils import download_directory, is_installed


def setup() -> None:
    update_package_manager()
    install_packages()
    cleanup_after_install()


def install_packages() -> None:
    download_directory(Path.packages)
    installations = {"packages": None, "snap": "snap install"}
    for name, command in installations.items():
        path = (Path.packages / name).with_suffix(".yaml")
        packages: list[str] = path.yaml
        cli.install(*packages, install_command=command)

    if not context.apt_is_installed:
        commands = "sudo pacman -S --noconfirm base-devel", "uv pip install wheel"
        cli.run_commands(*commands)


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
