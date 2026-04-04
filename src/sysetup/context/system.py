import platform

import cli


def is_mac() -> bool:
    return platform.system() == "Darwin"


def is_linux() -> bool:
    return platform.system() == "Linux"


def is_installed(package: str) -> bool:
    return cli.completes_successfully("which", package)
