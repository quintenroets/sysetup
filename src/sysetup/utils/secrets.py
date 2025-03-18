import json
import os
from typing import cast

import cli

from sysetup.context.context import context


def fetch_secret(name: str) -> str:
    email = os.environ["EMAIL"]
    if "BW_SESSION" not in os.environ:
        output = cli.capture_output(f"bw login {email} {context.options.password}")
        os.environ["BW_SESSION"] = output.split("--session ")[-1]
    response = cli.capture_output(f"bw list items --search {name}")
    secret = json.loads(response)[0]["notes"]
    return cast(str, secret)
