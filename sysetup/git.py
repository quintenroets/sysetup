import os

from github import Github
from tqdm import tqdm

import cli
from libs.threading import Threads

from .path import Path


def setup():
    g = Github(os.environ["gittoken"])
    user = g.get_user()
    repos = list(user.get_repos())
    progress = tqdm(repos, desc="Cloning repos")
    Threads(check_repo, repos, user=user, progress=progress).join()

    local_repos = list(Path.scripts.rglob("setup.py"))
    for setup in tqdm(local_repos, "Reinstalling editable repos"):
        cli.get("pip3 install --force-reinstall --no-deps -e", setup.parent)
    if Path.scripts.exists():
        (Path.scripts / "assets").symlink_to(Path.script_assets)


def check_repo(repo, user, progress):
    collabs = repo.get_collaborators()
    if collabs.totalCount == 1 and collabs[0].login == user.login and not repo.archived:
        name = repo.name.lower()
        if not list(Path.scripts.rglob(f"{name}/.git")):
            url = add_password(repo.clone_url)
            path = Path.scripts / name
            cli.get("git clone", url, path)
            if (path / "setup.py").exists():
                cli.get("pip3 install -e", path)
    progress.update()


def add_password(url):
    return url.replace("https://", f"https://{os.environ['gittoken']}@")


if __name__ == "__main__":
    setup()
