import cli
from superpathlib import Path

from sysetup.bitwarden import bitwarden_client
from sysetup.context import context, is_installed
from sysetup.packages import install_packages


def setup() -> None:
    enable_sudo()
    update_package_manager()
    install_packages()
    cleanup_after_install()


def enable_sudo() -> None:
    password = bitwarden_client().fetch_secret("Laptop")
    cli.run("sudo -S true", input=password)


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
    if not context.is_running_in_container:
        cli.run("tlp start", root=True)
    if is_installed("qdbus"):
        commands = "rm /usr/bin/qdbus", "ln -s /usr/lib/qt6/bin/qdbus /usr/bin/qdbus"
        cli.run_commands(*commands, root=True)
    delete = "apt purge -y" if context.apt_is_installed else "pacman -R --noconfirm"
    commands = (
        "auto-cpufreq --install",
        f"{delete} firefox",
    )
    cli.run_commands(*commands, check=False, root=True)
