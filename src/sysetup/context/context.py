import os
from collections.abc import Iterator
from functools import cached_property

import cli
from package_utils.context import Context as Context_

from sysetup.models import Options


class Context(Context_[Options, None, None]):
    @cached_property
    def package_manager(self) -> str:
        def generate_package_manager() -> Iterator[str]:
            package_managers = "apt-get", "pacman"
            for package_manager in package_managers:
                if cli.completes_successfully("which", package_manager):
                    yield package_manager

        return next(generate_package_manager())

    @cached_property
    def apt_is_installed(self) -> bool:
        return self.package_manager == "apt-get"

    @cached_property
    def is_running_in_test(self) -> bool:
        return "DISPLAY" not in os.environ


context = Context(Options)
