import io
import json
import os
import zipfile
from typing import cast

import cli
import requests
from dotenv import load_dotenv

from sysetup.context import context
from sysetup.models import Path
from sysetup.utils import download_file


def setup() -> None:
    os.environ["GITHUB"] = fetch_secret("GitHub")
    os.environ["RCLONE"] = fetch_secret("Rclone")
    download_file(Path("etc") / "environment")
    if "SUDO_ASKPASS" not in os.environ:
        download_file(Path.profile)
        load_dotenv(dotenv_path=Path.profile)


def fetch_secret(name: str) -> str:
    if not Path("bw").exists():
        download_bitwarden_cli()
    email = os.environ.get("EMAIL", "quinten.roets@gmail.com")
    if "BW_SESSION" not in os.environ:
        output = cli.capture_output(f"./bw login {email} {context.options.password}")
        os.environ["BW_SESSION"] = output.split("--session ")[-1]
    response = cli.capture_output(f"./bw list items --search {name}")
    secret = json.loads(response)[0]["notes"]
    return cast(str, secret)


def download_bitwarden_cli() -> None:
    url = "https://bitwarden.com/download/?app=cli&platform=linux"
    response = requests.get(url, timeout=10).content
    zip_bytes = io.BytesIO(response)
    with zipfile.ZipFile(zip_bytes, "r") as zip_file:
        for file_name in zip_file.namelist():
            path = Path(file_name)
            with zip_file.open(file_name) as extracted_file, path.open("wb") as fp:
                fp.write(extracted_file.read())
    Path("bw").chmod(0o755)
