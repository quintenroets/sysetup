# Sysetup
[![PyPI version](https://badge.fury.io/py/sysetup.svg)](https://badge.fury.io/py/sysetup)
![Python version](https://img.shields.io/badge/python-3.10+-brightgreen)
![Operating system](https://img.shields.io/badge/os-linux%20%7c%20macOS%20%7c%20windows-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
## [Plasma](https://kde.org/plasma-desktop/) 5.22 required

[Setup info](docs/setup-plasma.md)

## Setup steps
1) Run
   ```shell
   wget -O - https://raw.githubusercontent.com/quintenroets/sysetup/main/bin/setup | bash
   ```
   give rclone password when prompted
2) Appearance
    * Set wallpaper
    * Select We10OSX Cursors
3) Configure autocpufreq
4) Setup Chrome
    * Enable GPU acceleration in chrome://flags
    * PDF viewer: set page zoom to page fit
    * Import certificate from Scripts/assets/sysetup/certificates/certificate.crt
5) Login to
    * Pycharm professional
    * VNC Server
6) For new device: set touchpad scroll direction and click on touch
## Usage

## Installation
```shell
pip install sysetup
```
