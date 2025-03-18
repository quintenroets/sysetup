import os

import cli

from sysetup.context import context
from sysetup.models import Path
from sysetup.utils import download_file, is_installed


def setup() -> None:
    install_chromium()
    install_keyd()
    install_ydotool()
    download_file(Path("/") / "etc" / "systemd" / "system" / "ydotoold.service")
    enable_service("ssh")
    install_language_support()
    install_personal_git_repositories()


def install_personal_git_repositories() -> None:
    base_url = "https://github.com/quintenroets"
    token = os.getenv("GITHUB", None)
    if token is not None:
        base_url = base_url.replace("github.com", f"{token}@github.com")
    if not Path.extensions.exists():
        command = f"git clone {base_url}/extensions.git"
        cli.run(command, Path.extensions)
    cli.run(f"uv pip install git+{base_url}/system.git")


def install_language_support() -> None:
    try:
        packages = cli.capture_output("check-language-support")
    except FileNotFoundError:
        pass
    else:
        if packages:
            cli.install(packages)


def install_chromium() -> None:
    if not is_installed("chromium-browser"):
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
    check = not context.is_running_in_test
    cli.run_commands(*commands, shell=True, root=True, check=check)  # noqa: S604


def install_keyd() -> None:
    install_repository("keyd", "rvaiya/keyd")
    enable_service("keyd")


def enable_service(name: str) -> None:
    if not context.is_running_in_test:
        command = f"systemctl enable --now {name}"
        cli.run(command, root=True)


def install_repository(name: str, repository: str) -> None:
    if not is_installed(name):
        url = f"https://github.com/{repository}"
        with Path.tempdir() as directory:
            cli.run("git clone", url, directory)
            if (directory / "CMakeLists.txt").exists():
                cli.run("apt-get install cmake", root=True)
                cli.run("cmake .")
            cli.run_commands("make", "sudo make install", cwd=directory)


def install_ydotool() -> None:
    if not is_installed("ydotool"):
        cli.run("apt-get install scdoc")
        install_repository("ydotool", "ReimuNotMoe/ydotool")
        enable_service("ydotoold")
