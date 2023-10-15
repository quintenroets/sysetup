[![PyPI version](https://badge.fury.io/py/sysetup.svg)](https://badge.fury.io/py/sysetup)

## [Plasma](https://kde.org/plasma-desktop/) 5.22 required

[Setup info](docs/setup-plasma.md)

## Setup steps
1) Run
   ```shell
   wget -O - https://raw.githubusercontent.com/quintenroets/sysetup/main/bin/setup | bash
   ```
   give rclone password when prompted
2) Setup Chrome
   * Enable GPU acceleration in chrome://flags
   * PDF viewer: set page zoom to page fit
   * Import certificate from Scripts/assets/sysetup/certificates/certificate.crt
   * Add Google search engine with url: http://www.google.com/search?q=%s
3) Login to
   * Pycharm professional
   * VNC Server
4) For new device: set touchpad scroll direction and click on touch
