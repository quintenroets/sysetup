import cli
from superpathlib import Path

from sysetup.context import is_linux, is_mac

from . import linux, packages
from .bitwarden import bitwarden_client


def main() -> None:
    """
    Personal system setup.
    """
    remove_clutter()
    if is_linux():
        linux.setup()
    elif is_mac():
        packages.install_packages()
    install_personal_git_repositories()


def remove_clutter() -> None:
    names = (
        "Desktop",
        "Downloads",
        "Music",
        "Pictures",
        "Public",
        "Templates",
        "Videos",
    )
    for name in names:
        path = Path.HOME / name
        path.rmtree(missing_ok=True)

    root = Path("/") if is_linux() else Path("/") / "opt" / "homebrew"
    nginx_path = root / "etc" / "nginx" / "sites-enabled" / "default"
    if nginx_path.exists():
        cli.run("rm", nginx_path, root=True)


def install_personal_git_repositories() -> None:
    github_token = bitwarden_client().fetch_secret("github token")
    url = f"git+https://{github_token}@github.com/quintenroets/system.git"
    cli.run("uv pip install", url)
