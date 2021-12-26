from github import Github
import os

from libs.cli import Cli
from libs.path import Path

def setup():
    g = Github(
        os.environ["gittoken"]
        )
    user = g.get_user()

    for repo in user.get_repos():
        collabs = repo.get_collaborators()
        if collabs.totalCount == 1 and collabs[0].login == user.login and not repo.archived:
            url = add_password(repo.clone_url)
            try:
                Cli.get(f"pip install git+{url}")
            except:
                pass # can fail if not python project
            else:
                print(f"Installed {repo.name}")


def setup_repo(repo):
    path = Path.scripts / repo.name.lower()
    if not path.exists():
        print(path)
        url = add_password(repo.clone_url)
        Cli.run(f"git clone {url} {path}")
        if list(path.glob("setup.py")):
            Cli.run(f"pip3 install -e {path}")


def add_password(url):
    return url.replace("https://", f"https://{os.environ['gittoken']}@")

if __name__ == "__main__":
    setup()
