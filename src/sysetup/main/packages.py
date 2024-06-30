import cli

from sysetup.context import context
from sysetup.models import Path
from sysetup.utils import download_directory


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


def update_package_manager() -> None:
    if context.apt_is_installed:
        update_apt()
    else:
        cli.run("pacman -Syy", root=True)


def update_apt() -> None:
    agree_eula_command = (
        "echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula"
        "select true | sudo debconf-set-selections"
    )
    commands = ["sudo apt-get update", agree_eula_command]
    cli.run_commands_in_shell(*commands)
    if not Path("/snap").exists():
        cli.run("ln -s /var/lib/snapd/snap /snap", root=True)


def cleanup_after_install() -> None:
    after_install_command = (
        "sudo apt-get autoremove -y"
        if context.apt_is_installed
        else (
            "sudo pacman -S --noconfirm python-pip; sudo pacman -S --noconfirm"
            " base-devel; pip install wheel"
        )
    )
    cli.run_commands_in_shell(after_install_command, "sudo tlp start")
    cli.run("systemctl enable ssh", root=True)  # start ssh server before log in
    delete = "apt purge -y" if context.apt_is_installed else "pacman -R --noconfirm"
    commands = (
        "auto-cpufreq --install",  # Fails on VM
        f"{delete} firefox",  # fails if firefox not installed
    )
    cli.run_commands(*commands, check=False, root=True)
