import cli
from superpathlib import Path

from sysetup.context import is_installed
from sysetup.packages import install


def setup() -> None:
    install_repository("keyd", "rvaiya/keyd")
    install_repository("ydotool", "ReimuNotMoe/ydotool")
    enable_service("ssh")
    install_language_support()


def install_language_support() -> None:
    try:
        packages = cli.capture_output("check-language-support")
    except FileNotFoundError:
        pass
    else:
        if packages:
            install(packages)


def install_repository(name: str, repository: str) -> None:
    if not is_installed(name):
        if name == "ydotool":
            cli.run("apt-get install scdoc", root=True)
        url = f"https://github.com/{repository}"
        with Path.tempdir() as directory:
            cli.run("git clone", url, directory)
            if (directory / "CMakeLists.txt").exists():
                cli.run("apt-get install -y cmake", root=True)
                cli.run("cmake .", cwd=directory)
            cli.run_commands("make", "sudo make install", cwd=directory)
        enable_service(name)


def enable_service(name: str) -> None:
    if Path("/run/systemd/system").exists():
        cli.run(f"systemctl enable --now {name}", root=True)
