import os

from dotenv import load_dotenv

from sysetup.models import Path
from sysetup.utils import download_file


def setup() -> None:
    download_file(Path("etc") / "environment")
    if "SUDO_ASKPASS" not in os.environ:
        download_file(Path.profile)
        load_dotenv(dotenv_path=Path.profile)
