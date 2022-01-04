import argparse
import os

from libs.cli import Cli

from backup.backup import Backup

from . import installer, git, files


def setup():
    if "pw" in os.environ:
        setup_in_env()
    else:
        # download and load core config
        Backup().download("/.**", "- /.config/browser/*", quiet=False)
        Cli.run("source ~/.bash_profile", "sysetup")


def setup_in_env():
    files.setup()
    installer.setup()
    git.setup()
    Cli.run("sudo reboot now")


def main():
    parser = argparse.ArgumentParser(description='Setup OS')
    parser.add_argument(
        'action', nargs="?", help='The setup action to do: [all(default), files, install, git]', default="all"
    )

    args = parser.parse_args()
    action_mapper = {
        "all": setup,
        "files": files.setup,
        "install": installer.setup,
        "git": git.setup
        }
    action = action_mapper[args.action]
    action()


if __name__ == "__main__":
    main()
