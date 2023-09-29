import re

import cli
import requests

from .path import Path


def setup():
    package_manager = "apt" if "apt" in cli.get_install_command() else "pacman"
    update_package_manager(package_manager)
    install()
    if not cli.get("which jumpapp", check=False):
        install_jumpapp()
    if not cli.get("which chromium-browser", check=False):
        install_chromium()
    if not Path.extensions.exists():
        command = "git clone https://github.com/quintenroets/extensions"
        cli.run(command, cwd=Path.extensions.parent)
    install_notebook_extensions()
    # install_vpn()
    if not cli.is_success("which /etc/vnc/vncservice"):
        install_vnc()

    if not Path.linter_env.exists():
        install_linter_env()

    after_install(package_manager)


def install_chromium():
    commands = (
        "sudo add-apt-repository -y ppa:phd/chromium-browser",
        """echo '
Package: *
Pin: release o=LP-PPA-phd-chromium-browser
Pin-Priority: 1001
' | sudo tee /etc/apt/preferences.d/phd-chromium-browser""",
        "sudo apt install chromium-browser chromium-chromedriver",
    )
    cli.run_commands(*commands, shell=True)


def install_linter_env():
    linter_env_path = Path.HOME / ".local" / "share" / "envs" / "linterenv"
    if not linter_env_path.exists():
        cli.run("python -m venv", linter_env_path)
        python_path = linter_env_path / "bin" / "python"
        cli.run(f"{python_path} -m pip install autoimport tbhandler")


def install():
    installations = {
        "packages": None,
        "snap": "snap install",
    }
    for name, command in installations.items():
        path = (Path.packages / name).with_suffix(".yaml")
        packages: list = path.yaml
        cli.install(*packages, installer_command=command)


def update_package_manager(package_manager):
    if package_manager == "apt":
        cli.sh(
            "sudo apt update",
            # agree eula
            (
                "echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula"
                "select true | sudo debconf-set-selections"
            ),
            "sudo systemctl enable --now snapd.socket",
            # snap currently doesnt work on arm
        )
        if not Path("/snap").exists():
            cli.run("ln -s /var/lib/snapd/snap /snap", root=True)
    elif package_manager == "pacman":
        cli.run("pacman -Syy", root=True)
    else:
        raise Exception("No package manager found")


def after_install(package_manager):
    after_install_command = (
        "sudo apt autoremove -y"
        if package_manager == "apt"
        else (
            "sudo pacman -S --noconfirm python-pip; sudo pacman -S --noconfirm"
            " base-devel; pip install wheel"
        )
    )
    cli.sh(after_install_command, "sudo tlp start")
    cli.run("systemctl enable ssh", root=True)  # start ssh server before log in

    delete = "apt purge -y" if package_manager == "apt" else "pacman -R --noconfirm"
    cli.run_commands(
        "auto-cpufreq --install",  # Fails on VM
        f"{delete} firefox",  # fails if firefox not installed
        check=False,
        root=True,
    )


def install_jumpapp():
    cli.run("git clone https://github.com/mkropat/jumpapp")
    cli.run_commands("make", "sudo make install", cwd="jumpapp")
    cli.run("rm -rf jumpapp")


def install_vnc():
    download_url = get_vnc_download_url()
    version = download_url.split("files/")[1]

    # download and extract vnc server
    cli.run_commands(
        f"wget {download_url}", f"sudo dpkg -i {version}", capture_output=True
    )
    Path(version).unlink()

    cli.run_commands(
        "sudo systemctl enable vncserver-virtuald.service",
        "sudo systemctl start vncserver-virtuald.service",
        "/etc/vnc/vncservice start vncserver-x11-serviced",
        # start server before login
        "sudo systemctl enable vncserver-x11-serviced.service",
        # login with $email:($pw)vnc
        # now both realvnc and tigervnc (trough apt) are available
    )

    version = "VNC-Viewer-6.21.406-Linux-x86.deb"
    return  # todo: fix to 64 bit version
    cli.run(
        f"wget https://www.realvnc.com/download/file/viewer.files/{version}",
        f"sudo dpkg -i {version}",
    )
    version.unlink()


def get_vnc_download_url():
    download_page_url = "https://www.realvnc.com/en/connect/download/vnc/"
    download_page = requests.get(download_page_url).text
    download_url = re.search("https://.*Linux-x64.deb", download_page).group()
    return download_url


def install_vpn():
    cli.sh(
        "sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key FDC247B7",
        (
            'echo "deb https://repo.windscribe.com/ubuntu bionic main" | sudo tee'
            " /etc/apt/sources.list.d/windscribe-repo.list"
        ),
        "install windscribe-cli",
    )
    # login: $email2


def install_notebook_extensions():
    if not cli.get("which jupyter", check=False):
        cli.run("pip3 install jupyterlab")

    folder = Path(cli.get("jupyter --data-dir")) / "vim_binding"
    if not folder.exists():
        folder.parent.mkdir(parents=True, exist_ok=True)
        cli.run(
            f"git clone https://github.com/lambdalisue/jupyter-vim-binding {folder}"
        )


if __name__ == "__main__":
    setup()
