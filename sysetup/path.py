from libs.path import Path

Path.root = Path.assets / Path(__file__).parent.name
Path.packages = Path.root / "packages"
