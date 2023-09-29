[![PyPI version](https://badge.fury.io/py/sysetup.svg)](https://badge.fury.io/py/sysetup)

## [Plasma](https://kde.org/plasma-desktop/) 5.22 required

[Setup info](docs/setup-plasma.md)

## Setup steps
1) Set display size (1920 x 1080)
2) Run
   ```shell
   curl https://raw.githubusercontent.com/quintenroets/sysetup/main/bin/setup | bash
   ```
   password will need to be given once again for gpg decryption
3) Change wallpaper
4) Appearance
   * Select We10XOS cursors
   * Select Sugar Candy SDDM
   * Reapply window decorations
5) Setup Chrome
   * Enable GPU acceleration in chrome://flags
   * PDF viewer: set page zoom to page fit
6) Login to
   * Pycharm professional
   * VNC Server
7) connect bluetooth keyboard and run sysetup again to trust the device (auto connect on boot)
8) Manually copy plasma-org.kde.plasma.desktop-appletsrc
9) Set user avatar from sysetup assets > icons > avatar.jpg
10) Set kate vim mappings
