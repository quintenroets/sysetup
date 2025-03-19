import os

import cli
from backup.context import context as backup_context

from sysetup.context import context
from sysetup.models import Action

from . import files, installations, packages


def main() -> None:
    """
    Personal system setup.
    """
    set_backup_password()
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


def set_backup_password() -> None:
    try:
        assert backup_context.secrets.rclone
    except cli.models.CalledProcessError:
        os.environ["RCLONE"] = "dummy"
        backup_context.secrets.rclone = context.bitwarden.fetch_secret("Rclone")
