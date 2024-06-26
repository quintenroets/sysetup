from enum import Enum


class Action(str, Enum):
    all = "all"
    files = "files"
    install = "install"
    env = "env"
