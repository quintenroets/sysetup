import argparse

from libs.cli import Cli

from . import env, installer, git, files


def setup():
    env.setup()
    files.setup()
    installer.setup()
    git.setup()
    Cli.run("sudo reboot now")


def main():
    parser = argparse.ArgumentParser(description='Setup OS')
    parser.add_argument(
        'action', nargs="?", help='The setup action to do: [all(default), files, install, git, env]', default="all"
    )

    args = parser.parse_args()
    action_mapper = {
        "all": setup,
        "files": files.setup,
        "install": installer.setup,
        "git": git.setup,
        "env": env.setup
        }
    action = action_mapper[args.action]
    action()


if __name__ == "__main__":
    main()
