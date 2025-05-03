import os
from functools import cached_property

<<<<<<< HEAD
from package_utils.context import Context as Context_
=======
from .config import Config
from .options import Options
from .secrets_ import Secrets
>>>>>>> template

from sysetup.models import Options

from .installations import is_installed


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


context = Context(Options)
