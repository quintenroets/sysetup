import cli

from sysetup.context import context
from sysetup.context.system import is_linux
from sysetup.models import Path
from sysetup.utils import bitwarden_client, download_directory

from . import files, installations, packages


def main() -> None:
    """
    Personal system setup.
    """
    files.configure_git()
    files.configure_ssh()
    install_personal_git_repositories()
    files.remove_clutter()
    if is_linux():
        setup_linux()
    if not context.is_running_in_test:
        download_all_files()


def setup_linux() -> None:
    download_directory(Path.assets)
    files.set_background()
    files.install_crontab()
    packages.setup()
    installations.setup()


def install_personal_git_repositories() -> None:
    github_token = bitwarden_client().fetch_secret("GitHub")
    base_url = f"https://{github_token}@github.com/quintenroets"
    if not Path.extensions.exists():
        command = f"git clone {base_url}/extensions.git"
        cli.run(command, Path.extensions)
    cli.run(f"uv pip install git+{base_url}/system.git")


def download_all_files() -> None:
    download_directory(Path.assets.parent / "backup")
    flags = ("--include-browser",) if is_linux() else ()
    cli.run("backup pull --no-confirm-push", *flags)
