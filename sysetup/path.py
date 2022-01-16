from plib import Path as BasePath


class Path(BasePath):
    assets = BasePath.assets / 'sysetup'
    packages = assets / 'packages'
