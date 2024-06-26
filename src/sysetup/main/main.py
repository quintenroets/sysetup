import cli

from ..context import context
from ..models import Action
from . import environment, files, installer


def main() -> None:
    """
    Personal system setup.
    """
    action_mapper = {
        Action.all.value: setup,
        Action.files.value: files.setup,
        Action.install.value: installer.setup,
        Action.env.value: environment.setup,
    }
    action = action_mapper[context.options.action.value]
    action()


def setup() -> None:
    environment.setup()
    files.setup()
    installer.setup()
    cli.run("reboot now", root=True)
