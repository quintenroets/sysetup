import cli

from sysetup.context import context
from sysetup.models import Action

from . import environment, files, installations, packages


def main() -> None:
    """
    Personal system setup.
    """
    action_mapper = {
        Action.all.value: setup,
        Action.env.value: environment.setup,
        Action.files.value: files.setup,
        Action.install.value: installations.setup,
        Action.packages.value: packages.setup,
    }
    action = action_mapper[context.options.action.value]
    action()


def setup() -> None:
    environment.setup()
    packages.setup()
    files.setup()
    installations.setup()
    if not context.options.run_testing:
        cli.run("reboot now", root=True)
