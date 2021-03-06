#### Setup commands
```shell
sudo apt install -y git python3-pip;
export PATH=$PATH:~/.local/bin;
pip install git+https://github.com/quintenroets/sysetup;
sysetup;
```

## Plasma version 5.22 required

#### Ubuntu
1) Install kubuntu desktop: sudo apt install -y kubuntu-desktop

#### Newest Kubuntu
1) sudo add-apt-repository -y ppa:kubuntu-ppa/backports; sudo apt -y update && sudo apt -y full-upgrade; reboot

#### Raspberry Pi Manjaro 21.02
1) Run in tty: sudo pacman -Syu
2) Set display size (1920 x 1080)
3) General steps
4) Change tigervnc autostart to x0vncserver -passwordfile ~/.vnc/passwd -SecurityTypes=TLSVnc -localhost -display :0

#### Raspberry Pi Ubuntu21.04 Server
1) Run sudo apt update; sudo apt upgrade; sudo apt install kubuntu-desktop
2) Reboot and run startx in new tty to boot
3) Change username: https://www.linuxuprising.com/2019/04/how-to-change-username-on-ubuntu-debian.html
4) Newest kubuntu steps

## Manual steps
1) Set display size (1920 x 1080)
2) Execute setup command: password will need to be given once again for gpg decryption
3) Change wallpaper
4) Appearance
      * Select We10XOS cursors
      * Select sugar candy sddm
      * Reapply window decorations
5) Setup Chrome
      * Enable GPU acceleration in chrome://flags
      * PDF viewer: set page zoom to page fit
6) Pycharm professional: login with $email/$pw
7) VNC Server: login with $email/$pw
8) connect bluetooth keyboard and run sysetup again to trust the device (auto connect on boot)
9) Manually copy plasma-org.kde.plasma.desktop-appletsrc
10) Set user avatar from sysetup assets > icons > avatar.jpg
