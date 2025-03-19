import os
from functools import cached_property

from package_utils.context import Context as Context_
from rich.prompt import Prompt

from sysetup.models import Options
from sysetup.utils import is_installed
from sysetup.utils.bitwarden import Bitwarden


class Context(Context_[Options, None, None]):
    @cached_property
    def package_manager(self) -> str:
        options = "apt-get", "pacman"
        return next(option for option in options if is_installed(option))

    @cached_property
    def apt_is_installed(self) -> bool:
        return self.package_manager == "apt-get"

    @cached_property
    def is_running_in_test(self) -> bool:
        return "DISPLAY" not in os.environ

    @cached_property
    def bitwarden(self) -> Bitwarden:
        password = self.options.bitwarden_password or Prompt.ask(
            "Bitwarden password",
            password=True,
        )
        return Bitwarden(password=password, email=self.options.bitwarden_email)


context = Context(Options)
