from github import Github
import os

from libs.cli import Cli
from libs import folders

def setup():
    g = Github(
        os.environ["gittoken"]
        )
    user = g.get_user()
    username = user.login
    config = {
        "user.name": username,
        "user.email": os.environ["email"],
        "pull.rebase": "false"
    }
    Cli.run(f"git config --global {k} '{v}'" for k, v in config.items())

    skip_repos = ["old", "archive"]
    
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
