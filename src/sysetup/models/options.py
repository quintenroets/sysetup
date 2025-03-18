from dataclasses import dataclass
from typing import Annotated

import typer

from .action import Action


@dataclass
class Options:
    password: Annotated[str, typer.Option(help="The login and bitwarden password")] = ""
    action: Annotated[Action, typer.Argument(help="The part to setup")] = Action.all
