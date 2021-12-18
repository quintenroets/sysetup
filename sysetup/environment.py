import crypt
import getpass
import os

from libs.cli import Cli
from libs.parser import Parser
from libs import folders

from .filemanager import FileManager


def setup():
    return
    if "pw" not in os.environ:
        setup_environment()


def setup_environment():
    pwd = getpass.getpass()
    while not is_correct(pwd):
        pwd = getpass.getpass()

    home = os.path.expanduser("~")
    docs = os.path.join(home, "Documents")
    scripts = os.path.join(docs, "Scripts")

    env_variables = {
        "pw": pwd,
        "home": home,
        "docs": docs,
        "scripts": scripts
    }

    content = "\n".join([f'export {key}="{value}"' for key, value in env_variables.items()])
    profile_file = FileManager.save(content, home, ".bash_profile")
    Cli.run(f"source '{profile_file}'")


def is_correct(pwd):
    os.environ["pw"] = pwd
    try:
        Cli.get("echo invalid | sudo -S ls") # give wrong password if not already filled in by cli
    except:
        correct = False
    else:
        correct = True
    return correct


if __name__ == "__main__":
    setup()
