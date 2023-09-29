## Plasma setup

#### Ubuntu
Install kubuntu desktop
   ```shell
   sudo apt install -y kubuntu-desktop
   ```
Latest version
   ```shell
   sudo add-apt-repository -y ppa:kubuntu-ppa/backports
   sudo apt -y update
   sudo apt -y full-upgrade
   reboot
   ```

#### Raspberry Pi Manjaro 21.02
1) Run
   ```shell
   sudo pacman -Syu
   ```
2) Set display size (1920 x 1080)
3) General steps
4) Change TigerVNC autostart to:
   ```shell
   x0vncserver -passwordfile ~/.vnc/passwd -SecurityTypes=TLSVnc -localhost -display :0
   ```

#### Raspberry Pi Ubuntu21.04 Server
1) Run
   ```shell
   sudo apt update
   sudo apt upgrade
   sudo apt install kubuntu-desktop
   ```
2) Reboot and run in new tty:
   ```shell
   startx
   ```
   to boot
3) Change username: [tutorial](https://www.linuxuprising.com/2019/04/how-to-change-username-on-ubuntu-debian.html)
4) Newest kubuntu steps
