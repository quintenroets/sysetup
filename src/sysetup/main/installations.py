import cli

from sysetup.context import context
from sysetup.models import Path
from sysetup.utils import bitwarden, is_installed

from .packages import install


def setup() -> None:
    install_chromium()
    install_keyd()
    install_ydotool()
    enable_service("ssh")
    install_language_support()
    install_personal_git_repositories()


def install_personal_git_repositories() -> None:
    github_token = bitwarden.client.fetch_secret("GitHub")
    base_url = f"https://{github_token}@github.com/quintenroets"
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
            install(packages)


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
    install_custom_certificate()


def install_custom_certificate() -> None:
    install(["libnss3-tools"])
    certificate_directory = Path.HOME / ".pki" / "nssdb"
    certificate_file = Path.assets / "certificates" / "certificate.crt"
    command = (
        f"certutil -d sql:{certificate_directory} "
        f'-A -t "C,," -n "QCA" -i {certificate_file}'
    )
    if not context.is_running_in_test:
        cli.run(command)


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
                cli.run("apt-get install -y cmake", root=True)
                cli.run("cmake .", cwd=directory)
            cli.run_commands("make", "sudo make install", cwd=directory)


def install_ydotool() -> None:
    if not is_installed("ydotool"):
        cli.run("apt-get install scdoc", root=True)
        install_repository("ydotool", "ReimuNotMoe/ydotool")
        enable_service("ydotoold")
