from enum import Enum


class Action(str, Enum):
    all = "all"
    files = "files"
    packages = "packages"
    install = "install"
    env = "env"
