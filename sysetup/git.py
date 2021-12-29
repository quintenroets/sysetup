from github import Github
import os
from tqdm import tqdm

from libs.cli import Cli
from libs.threading import Threads
from .path import Path

def setup():
    g = Github(
        os.environ["gittoken"]
        )
    user = g.get_user()
    repos = user.get_repos()
    progress = tqdm("Checking repos")
    Threads(check_repo, repos, user=user, progress=progress).join()
    for setup in tqdm(Path.scripts.rglob("setup.py"), "Installing repos locally"):
        Cli.run(f"pip3 install --force-reinstall --no-deps -e {setup.parent}")
        

def check_repo(repo, user, progress): 
    collabs = repo.get_collaborators()
    if collabs.totalCount == 1 and collabs[0].login == user.login and not repo.archived:
        name = repo.name.lower()
        if not list(Path.scripts.rglob(f"{name}/.git")):
            url = add_password(repo.clone_url)
            Cli.get(f"git clone {url} {Path.scripts / name}")
            if (path / "setup.py").exists():
                Cli.get(f"pip3 install -e {path}")
    progress.update()


def add_password(url):
    return url.replace("https://", f"https://{os.environ['gittoken']}@")

if __name__ == "__main__":
    setup()
