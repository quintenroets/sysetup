from libs.path import Path

assets = Path.assets / Path(__file__).parent.name
Path.packages = assets / "packages"
