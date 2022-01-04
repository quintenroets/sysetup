from plib import Path as BasePath


class Path(BasePath):
    assets = BasePath.assets / BasePath(__file__).parent.name
    packages = assets / "packages"
