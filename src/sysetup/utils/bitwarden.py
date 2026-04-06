import io
import json
import sys
import zipfile
from dataclasses import dataclass
from functools import cache, cached_property
from typing import cast

import cli
import requests
from rich.prompt import Prompt

from sysetup.context import context
from sysetup.models import Path


@dataclass
class Client:
    password: str
    email: str

    def fetch_secret(self, name: str) -> str:
        command = "./bw list items --session", self.session_token, "--search", name
        response = cli.capture_output(*command)
        item = json.loads(response)[0]
        secret = item.get("notes") or item["login"]["password"]
        return cast("str", secret)

    @cached_property
    def session_token(self) -> str:
        if not Path("bw").exists():
            self.download_cli()

        logged_in = "userEmail" in cli.capture_output("./bw status")
        command: tuple[str, ...] = "./bw unlock --raw", self.password
        if not logged_in:
            if context.secrets.bw_clientid:
                cli.run("./bw login --apikey")
            else:
                command = "./bw login --raw", self.email, self.password
        return cli.capture_output(*command)

    def download_cli(self) -> None:
        platform = "macos" if sys.platform == "darwin" else "linux"
        download_url = f"https://bitwarden.com/download/?app=cli&platform={platform}"
        response = requests.get(download_url, timeout=10).content
        zip_bytes = io.BytesIO(response)
        with zipfile.ZipFile(zip_bytes, "r") as zip_file:
            zip_file.extractall()
        Path("bw").chmod(0o755)


@cache
def bitwarden_client() -> Client:
    password = context.options.bitwarden_password
    password = password or Prompt.ask("Bitwarden password", password=True)
    return Client(password=password, email=context.options.bitwarden_email)
