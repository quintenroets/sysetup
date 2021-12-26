import os
import shutil

from libs.cli import Cli

from .path import Path

def install(vpn=False):
    package_manager = Cli.get_package_manager()
    update_package_manager(package_manager)

    Cli.install(
        Path.packages.load("packages")
        )
    Cli.install(
        Path.packages.load("snap"),
        "snap install"
        )
    
    Cli.run(
        "sudo apt autoremove -y" if package_manager == "apt" else "sudo pacman -S --noconfirm python-pip; sudo pacman -S --noconfirm base-devel; pip install wheel",
        "sudo tlp start",
    )

    delete = "apt purge -y" if package_manager == "apt" else "pacman -R --noconfirm"
    Cli.run(
        (
            "sudo auto-cpufreq --install", # Fails on VM
            f"sudo {delete} firefox", # fails if firefox not installed
        ),
        check=False)
        
    install_jumpapp()
    if vpn:
        install_vpn()
    if not Cli.get("/etc/vnc/vncelevate -v", check=False):
        install_vnc()
        
def update_package_manager(package_manager):
    if package_manager == "apt":
        Cli.run(
            "sudo apt update",
            # agree eula
            "echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | sudo debconf-set-selections",
            "sudo systemctl enable --now snapd.socket",
            # snap currently doesnt work on arm
        )
        if not os.path.exists("/snap"):
            Cli.run("sudo ln -s /var/lib/snapd/snap /snap")
    elif package_manager == "pacman":
        Cli.run("sudo pacman -Syy")
    else:
        raise Exception("No package manager found")
    


def install_jumpapp():
    Cli.run("git clone https://github.com/mkropat/jumpapp", "cd jumpapp", "make", "sudo make install", "cd ..", "rm -rf jumpapp")


def install_vnc():
    version = "VNC-Server-6.7.4-Linux-x64-ANY.tar.gz"

    # download and extract vnc server
    Cli.get(
        f"wget https://www.realvnc.com/download/file/vnc.files/{version}",
        f"tar -xvzf {version}"
    )
    os.remove(version)

    vnc_folder = [folder for folder in os.listdir(".") if "VNC" in folder][0]
    os.chdir(vnc_folder)
    Cli.run(
        f"sudo ./vncinstall",
        "sudo systemctl enable vncserver-virtuald.service",
        "sudo systemctl start vncserver-virtuald.service",
        'sudo /etc/vnc/vncelevate "Enable VNC Server Service Mode" /etc/vnc/vncservice start vncserver-x11-serviced',
        # login with $email:($pw)vnc
        # now both realvnc and tigervnc (trough apt) are available
    )
    os.chdir("..")
    shutil.rmtree(vnc_folder)

    version = "VNC-Viewer-6.21.406-Linux-x86.deb"
    return # todo: fix to 64 bit version
    Cli.run(
        f"wget https://www.realvnc.com/download/file/viewer.files/{version}",
        f"sudo dpkg -i {version}"
    )
    os.remove(version)
    
def install_vpn():
    Cli.run(
        "sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key FDC247B7",
        "echo 'deb https://repo.windscribe.com/ubuntu bionic main' | sudo tee /etc/apt/sources.list.d/windscribe-repo.list",
        "install windscribe-cli"
    )
    # login: $email2


if __name__ == "__main__":
    install()
