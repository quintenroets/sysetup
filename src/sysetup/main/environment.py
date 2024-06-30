import os

from dotenv import load_dotenv

from sysetup.models import Path
from sysetup.utils import download_file


def setup() -> None:
    download_file(Path("etc") / "environment")
    if "SUDO_ASKPASS" not in os.environ:
        path = Path.HOME / ".bask_profile"
        download_file(Path.HOME / ".bask_profile")
        load_dotenv(dotenv_path=Path.HOME / path)
