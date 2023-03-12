from plib import Path as BasePath


class Path(BasePath):
    assets = BasePath.assets / "sysetup"
    packages = assets / "packages"
    linter_env = assets / "linterenv"
    extensions = BasePath.HOME / ".local" / "share" / "extensions"
