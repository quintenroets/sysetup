import argparse

import cli

from . import env, files, installer


def setup():
    env.setup()
    files.setup()
    installer.setup()
    cli.run("reboot now", root=True)


def main():
    parser = argparse.ArgumentParser(description="Setup OS")
    parser.add_argument(
        "action",
        nargs="?",
        help="The setup action to do: [all(default), files, install, env]",
        default="all",
    )

    args = parser.parse_args()
    action_mapper = {
        "all": setup,
        "files": files.setup,
        "install": installer.setup,
        "env": env.setup,
    }
    action = action_mapper[args.action]
    action()


if __name__ == "__main__":
    main()
