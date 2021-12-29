from github import Github
import os

from libs.cli import Cli
from .path import Path

def setup():
    g = Github(
        os.environ["gittoken"]
        )
    user = g.get_user()

    for repo in user.get_repos():
        collabs = repo.get_collaborators()
        if collabs.totalCount == 1 and collabs[0].login == user.login and not repo.archived:
            name = repo.name.lower()
            if not list(Path.scripts.rglob(f"{name}/.git")):
                url = add_password(repo.clone_url)
                Cli.run(f"git clone {url} {Path.scripts / name}")
                if (path / "setup.py").exists():
                    Cli.run(f"pip3 install -e {path}")
    
    for setup in Path.scripts.rglob("setup.py"):
        Cli.run(f"pip3 install --force-reinstall --no-deps -e {setup.parent}")


def add_password(url):
    return url.replace("https://", f"https://{os.environ['gittoken']}@")

if __name__ == "__main__":
    setup()
