from pathlib import Path

assets = Path.assets / Path(__file__).parent.name

class Path(Path):
    packages = assets / "packages"
