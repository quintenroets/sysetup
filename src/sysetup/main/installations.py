import os

import cli

from sysetup.context import context
from sysetup.models import Path


def setup() -> None:
    install_chromium()
    install_repository("jumpapp", "mkropat/jumpapp")
    install_keyd()
    install_language_support()
    install_linter_env()
    install_personal_git_repositories()


def install_personal_git_repositories() -> None:
    base_url = "https://github.com/quintenroets"
    token = os.getenv("GITHUB", None)
    if token is not None:
        base_url = base_url.replace("github.com", f"{token}@github.com")
    if not Path.extensions.exists():
        command = f"git clone {base_url}/extensions.git"
        cli.run(command, Path.extensions)
    cli.run(f"pip install git+{base_url}/system.git")


def install_language_support() -> None:
    try:
        packages = cli.capture_output("check-language-support")
    except FileNotFoundError:
        pass
    else:
        if packages:
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
    check = not context.is_running_in_test
    cli.run_commands(*commands, shell=True, root=True, check=check)  # noqa: S604


def install_linter_env() -> None:
    if not Path.linter_env.exists():
        cli.run("python -m venv", Path.linter_env.name, cwd=Path.linter_env.parent)
        python_path = Path.linter_env / "bin" / "python"
        cli.run(f"{python_path} -m pip install autoimport powertrace-hooks")


def install_keyd() -> None:
    install_repository("keyd", "rvaiya/keyd")
    commands = ("systemctl enable keyd", "sudo systemctl start keyd")
    if not context.is_running_in_test:
        cli.run_commands(*commands, root=True)


def install_repository(name: str, repository: str) -> None:
    if not cli.capture_output("which", name, check=False):
        url = f"https://github.com/{repository}"
        with Path.tempdir() as directory:
            cli.run("git clone", url, directory)
            cli.run_commands("make", "sudo make install", cwd=directory)
