import io
import json
import zipfile
from dataclasses import dataclass
from functools import cached_property
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
    download_url: str = "https://bitwarden.com/download/?app=cli&platform=linux"

    def fetch_secret(self, name: str) -> str:
        command = "./bw list items --session", self.session_token, "--search", name
        response = cli.capture_output(*command)
        secret = json.loads(response)[0]["notes"]
        return cast("str", secret)

    @cached_property
    def session_token(self) -> str:
        if not Path("bw").exists():
            self.download_cli()
        command: tuple[str, ...]
        if context.secrets.bw_clientid:
            cli.run("./bw login --apikey")
            command = "./bw unlock --raw", self.password
        else:
            command = "./bw login --raw", self.email, self.password
        return cli.capture_output(*command)

    def download_cli(self) -> None:
        response = requests.get(self.download_url, timeout=10).content
        zip_bytes = io.BytesIO(response)
        with zipfile.ZipFile(zip_bytes, "r") as zip_file:
            zip_file.extractall()
        Path("bw").chmod(0o755)


@dataclass
class Bitwarden:
    @cached_property
    def client(self) -> Client:
        password = context.options.bitwarden_password
        password = password or Prompt.ask("Bitwarden password", password=True)
        return Client(password=password, email=context.options.bitwarden_email)


bitwarden = Bitwarden()
