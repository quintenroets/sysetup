import cli

from sysetup.context import context
from sysetup.context.system import is_linux, is_mac
from sysetup.models import Path
from sysetup.utils import bitwarden_client

from . import files, linux, packages


def main() -> None:
    """
    Personal system setup.
    """
    files.setup()
    if is_linux():
        linux.setup()
    elif is_mac():
        packages.install_packages()
    install_personal_git_repositories()
    if not context.is_running_in_container:
        flags = ("--include-browser",) if is_linux() else ()
        cli.run("backup pull --no-confirm-push", *flags)


def install_personal_git_repositories() -> None:
    github_token = bitwarden_client().fetch_secret("GitHub Token")
    base_url = f"https://{github_token}@github.com/quintenroets"
    if not Path.extensions.exists():
        command = f"git clone {base_url}/extensions.git"
        cli.run(command, Path.extensions)
    cli.run(f"uv pip install git+{base_url}/system.git")
