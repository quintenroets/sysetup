import os
from dataclasses import dataclass, field


@dataclass
class Secrets:
    bw_clientid: str = field(default_factory=lambda: os.environ.get("BW_CLIENTID", ""))
    bw_clientsecret: str = field(
        default_factory=lambda: os.environ.get("BW_CLIENTSECRET", ""),
    )
