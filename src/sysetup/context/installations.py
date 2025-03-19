import cli


def is_installed(package: str) -> bool:
    return cli.completes_successfully("which", package)
