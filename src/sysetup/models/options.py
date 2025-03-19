from dataclasses import dataclass
from typing import Annotated

import typer

from .action import Action


@dataclass
class Options:
    bitwarden_password: Annotated[str, typer.Option()] = ""
    bitwarden_email: Annotated[str, typer.Option()] = "quinten.roets@gmail.com"
    action: Annotated[Action, typer.Argument(help="The part to setup")] = Action.all
