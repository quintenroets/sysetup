import getpass
from github import Github
import os

from libs.cli import Cli
from libs import folders

from . import constants

def setup():
    g = Github(
        os.environ["gittoken"]
        )
    config = {
        "user.name": getpass.getuser().capitalize(),
        "user.email": os.environ["email"],
        "pull.rebase": "false"
    }
    Cli.run(f"git config --global {k} '{v}'" for k, v in config.items())

    current_remote = Cli.get(f"cd {constants.ROOT_PATH}", "git config remote.origin.url")
    new_remote = add_password(current_remote)
    current_remote = Cli.run(f"cd {constants.ROOT_PATH}", f"git config remote.origin.url {new_remote}")

    skip_repos = ["old", "archive", "sysetup"]
    user = g.get_user()
    username = user.login
    
    repos = [
        repo
        for repo in user.get_repos() 
        if repo.get_collaborators().totalCount == 1 
        and repo.get_collaborators()[0].login == username
        and not any([w in repo.name.lower() for w in skip_repos])
        ]

    repo_commands = {
        "jumpapp": ["make", "sudo make install"]
        }
    
    for repo in repos:
        name = repo.name.lower()
        path = folders.scripts / name
        if not path.exists():
            url = add_password(repo.clone_url)
            Cli.run(f"git clone {url} {path}")

            commands = [
                f"cd {path}",
                *repo_commands.get(name, [])
                ]
            
            if list(path.glob("setup.py")):
                commands.append("pip3 install -e .")
            elif list(path.glob("requirements.txt")):
                commands.append("pip3 install -r requirements.txt")

            Cli.run(commands)
            
def add_password(url):
    return url.replace("https://", f"https://{os.environ['gittoken']}@")

if __name__ == "__main__":
    setup()
