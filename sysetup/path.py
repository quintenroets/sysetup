from plib import Path as BasePath

assets = BasePath.assets / BasePath(__file__).parent.name

class Path(BasePath):
    packages = assets / "packages"
