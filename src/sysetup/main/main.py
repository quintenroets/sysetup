import cli

from sysetup.context import Action, context

from . import files, installations, packages


def main() -> None:
    """
    Personal system setup.
    """
    action_mapper = {
        Action.all.value: setup,
        Action.packages.value: packages.setup,
        Action.files.value: files.setup,
        Action.install.value: installations.setup,
    }
    action = action_mapper[context.options.action.value]
    action()


def setup() -> None:
    packages.setup()
    files.setup()
    installations.setup()
    if not context.is_running_in_test:
        cli.run("backup pull --include-browser --no-confirm-push")
