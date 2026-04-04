from dataclasses import dataclass
from typing import Annotated

import typer


@dataclass
class Options:
    bitwarden_password: Annotated[str, typer.Option()] = ""
    bitwarden_email: Annotated[str, typer.Option()] = "quinten.roets@gmail.com"
