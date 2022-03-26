import cli

from .path import Path


def setup():
    package_manager = "apt" if "apt" in cli.get_install_command() else "pacman"
    update_package_manager(package_manager)
    install()
    install_jumpapp()
    install_notebook_extensions()
    # install_vpn()
    if not cli.get("/etc/vnc/vncelevate -v", check=False):
        install_vnc()

    after_install(package_manager)


def install():
    cli.install(*Path.packages.load("packages"))
    cli.install(*Path.packages.load("snap"), "snap install")


def update_package_manager(package_manager):
    if package_manager == "apt":
        cli.sh(
            "sudo apt update",
            # agree eula
            "echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | sudo debconf-set-selections",
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
        else "sudo pacman -S --noconfirm python-pip; sudo pacman -S --noconfirm base-devel; pip install wheel"
    )
    cli.sh(after_install_command, "sudo tlp start")

    delete = "apt purge -y" if package_manager == "apt" else "pacman -R --noconfirm"
    cli.run_commands(
        "auto-cpufreq --install",  # Fails on VM
        f"{delete} firefox",  # fails if firefox not installed
        check=False,
        root=True,
    )


def install_jumpapp():
    cli.install("pandoc")
    cli.run("git clone https://github.com/mkropat/jumpapp")
    cli.run_commands("make", "sudo make install", cwd="jumpapp")
    cli.run("rm -rf jumpapp")


def install_vnc():
    version = "VNC-Server-6.7.4-Linux-x64-ANY.tar.gz"

    # download and extract vnc server
    cli.run_commands(
        f"wget https://www.realvnc.com/download/file/vnc.files/{version}",
        f"tar -xvzf {version}",
        capture_output=True,
    )
    version.unlink()

    vnc_folder = next(iter(Path("").glob("*VNC*")))
    cli.run_commands(
        f"sudo ./vncinstall",
        "sudo systemctl enable vncserver-virtuald.service",
        "sudo systemctl start vncserver-virtuald.service",
        'sudo /etc/vnc/vncelevate "Enable VNC Server Service Mode" /etc/vnc/vncservice start vncserver-x11-serviced',
        # login with $email:($pw)vnc
        # now both realvnc and tigervnc (trough apt) are available
        cwd=vnc_folder,
    )
    vnc_folder.rmtree()

    version = "VNC-Viewer-6.21.406-Linux-x86.deb"
    return  # todo: fix to 64 bit version
    cli.run(
        f"wget https://www.realvnc.com/download/file/viewer.files/{version}",
        f"sudo dpkg -i {version}",
    )
    version.unlink()


def install_vpn():
    cli.sh(
        "sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key FDC247B7",
        'echo "deb https://repo.windscribe.com/ubuntu bionic main" | sudo tee /etc/apt/sources.list.d/windscribe-repo.list',
        "install windscribe-cli",
    )
    # login: $email2


def install_notebook_extensions():
    cli.run("pip3 install jupyterlab")
    folder = Path(cli.get("jupyter --data-dir")) / "vim_binding"
    folder.parent.mkdir(parents=True, exist_ok=True)
    folder.unlink(missing_ok=True)
    cli.run(f"git clone https://github.com/lambdalisue/jupyter-vim-binding {folder}")


if __name__ == "__main__":
    setup()
