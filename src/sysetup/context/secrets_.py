from dataclasses import dataclass


@dataclass
class Secrets:
    bw_clientid: str = ""
    bw_clientsecret: str = ""
