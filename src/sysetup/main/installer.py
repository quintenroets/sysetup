import cli
from cli.commands.install import extract_package_manager_command

from ..models import Path


def setup() -> None:
    package_manager = "apt" if "apt" in extract_package_manager_command() else "pacman"
    update_package_manager(package_manager)
    install()
    install_chromium()
    install_extensions()
    install_jumpapp()
    install_language_support()
    install_linter_env()
    after_install(package_manager)


def install_extensions() -> None:
    if not Path.extensions.exists():
        command = "git clone https://github.com/quintenroets/extensions"
        cli.run(command, cwd=Path.extensions.parent)


def install_language_support() -> None:
    packages = cli.capture_output("check-language-support")
    cli.install(packages)


def install_chromium() -> None:
    if not cli.capture_output("which chromium-browser", check=False):
        _install_chromium()


def _install_chromium() -> None:
    release_name = cli.capture_output_lines("lsb_release -sc")[-1]
    repo_url = f"https://freeshell.de/phd/chromium/{release_name}"
    commands = (
        f'echo "deb {repo_url} /" | sudo tee /etc/apt/sources.list.d/phd-chromium.list',
        "apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 869689FE09306074",
        "apt-get update",
        "apt-get install -y chromium",
    )
    cli.run_commands(*commands, shell=True, root=True)


def install_linter_env() -> None:
    if not Path.linter_env.exists():
        cli.run("python -m venv", Path.linter_env.name, cwd=Path.linter_env.parent)
        python_path = Path.linter_env / "bin" / "python"
        cli.run(f"{python_path} -m pip install autoimport powertrace-hooks")


def install() -> None:
    installations = {
        "packages": None,
        "snap": "snap install",
    }
    for name, command in installations.items():
        path = (Path.packages / name).with_suffix(".yaml")
        packages: list[str] = path.yaml
        cli.install(*packages, install_command=command)


def update_package_manager(package_manager: str) -> None:
    if package_manager == "apt":
        cli.run_commands_in_shell(
            "sudo apt update",
            # agree eula
            (
                "echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula"
                "select true | sudo debconf-set-selections"
            ),
            "sudo systemctl enable --now snapd.socket",
            # snap currently doesnt work on arm
        )
        if not Path("/snap").exists():
            cli.run("ln -s /var/lib/snapd/snap /snap", root=True)
    elif package_manager == "pacman":
        cli.run("pacman -Syy", root=True)
    else:
        raise Exception("No package manager found")


def after_install(package_manager: str) -> None:
    after_install_command = (
        "sudo apt autoremove -y"
        if package_manager == "apt"
        else (
            "sudo pacman -S --noconfirm python-pip; sudo pacman -S --noconfirm"
            " base-devel; pip install wheel"
        )
    )
    cli.run_commands_in_shell(after_install_command, "sudo tlp start")
    cli.run("systemctl enable ssh", root=True)  # start ssh server before log in

    delete = "apt purge -y" if package_manager == "apt" else "pacman -R --noconfirm"
    cli.run_commands(
        "auto-cpufreq --install",  # Fails on VM
        f"{delete} firefox",  # fails if firefox not installed
        check=False,
        root=True,
    )


def install_jumpapp() -> None:
    if not cli.capture_output("which jumpapp", check=False):
        cli.run("git clone https://github.com/mkropat/jumpapp")
        cli.run_commands("make", "sudo make install", cwd="jumpapp")
        cli.run("rm -rf jumpapp")


def install_vpn() -> None:
    add_source_command = (
        'echo "deb https://repo.windscribe.com/ubuntu bionic main" | sudo tee'
        " /etc/apt/sources.list.d/windscribe-repo.list"
    )
    commands = (
        "sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key FDC247B7",
        add_source_command,
        "install windscribe-cli",
    )
    cli.run_commands_in_shell(*commands)
    # login: $email2
