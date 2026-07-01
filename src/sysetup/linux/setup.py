from . import installations, packages


def setup() -> None:
    packages.setup()
    installations.setup()
