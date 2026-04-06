import cli

from sysetup.context import context
from sysetup.context.system import is_installed
from sysetup.main.packages import install
from sysetup.models import Path


def setup() -> None:
    if not is_installed("chromium-browser"):
        install_chromium()
    install_repository("keyd", "rvaiya/keyd")
    install_repository("ydotool", "ReimuNotMoe/ydotool")
    enable_service("ssh")
    install_language_support()


def install_language_support() -> None:
    try:
        packages = cli.capture_output("check-language-support")
    except FileNotFoundError:
        pass
    else:
        if packages:
            install(packages)


def install_chromium() -> None:
    release_name = cli.capture_output_lines("lsb_release -sc")[-1]
    repo_url = f"https://freeshell.de/phd/chromium/{release_name}"
    key = "869689FE09306074"
    keyring = "/usr/share/keyrings/phd-chromium.gpg"
    sources_file = "/etc/apt/sources.list.d/phd-chromium.list"
    commands = (
        f"gpg --keyserver keyserver.ubuntu.com --recv-keys {key}",
        f"gpg --export {key} | sudo gpg --dearmor -o {keyring}",
        f'echo "deb [signed-by={keyring}] {repo_url} /" | sudo tee {sources_file}',
        "apt-get update",
        "apt-get install -y chromium",
    )
    check = not context.is_running_in_test
    cli.run_commands(*commands, shell=True, root=True, check=check)  # noqa: S604


def install_repository(name: str, repository: str) -> None:
    if not is_installed(name):
        if name == "ydotool":
            cli.run("apt-get install scdoc", root=True)
        url = f"https://github.com/{repository}"
        with Path.tempdir() as directory:
            cli.run("git clone", url, directory)
            if (directory / "CMakeLists.txt").exists():
                cli.run("apt-get install -y cmake", root=True)
                cli.run("cmake .", cwd=directory)
            cli.run_commands("make", "sudo make install", cwd=directory)
        enable_service(name)


def enable_service(name: str) -> None:
    if not context.is_running_in_test:
        command = f"systemctl enable --now {name}"
        cli.run(command, root=True)
