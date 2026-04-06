from functools import cached_property
from pathlib import Path

from package_utils.context.context import Context as Context_

from .options import Options
from .secrets_ import Secrets
from .system import is_installed


class Context(Context_[Options, None, Secrets]):
    @cached_property
    def package_manager(self) -> str:
        options = "apt-get", "pacman"
        return next(option for option in options if is_installed(option))

    @cached_property
    def apt_is_installed(self) -> bool:
        return self.package_manager == "apt-get"

    @cached_property
    def is_running_in_container(self) -> bool:
        return Path("/.dockerenv").exists()


context = Context(Options, Secrets=Secrets)
