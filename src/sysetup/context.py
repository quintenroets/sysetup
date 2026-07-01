import os
import platform
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path

import cli
from package_utils.context.context import Context as Context_


@dataclass
class Options:
    bitwarden_email: str = "quinten.roets@gmail.com"


@dataclass
class Secrets:
    bitwarden: str
    bw_clientid: str = field(default_factory=lambda: os.environ.get("BW_CLIENTID", ""))


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

    @cached_property
    def package_install_command(self) -> str:
        return (
            "apt-get install -y" if self.apt_is_installed else "pacman -S --noconfirm"
        )


context = Context(Options, Secrets=Secrets)


def is_mac() -> bool:
    return platform.system() == "Darwin"


def is_linux() -> bool:
    return platform.system() == "Linux"


def is_installed(package: str) -> bool:
    return cli.completes_successfully("which", package)
