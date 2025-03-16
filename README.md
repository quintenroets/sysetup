# Sysetup
[![PyPI version](https://badge.fury.io/py/sysetup.svg)](https://badge.fury.io/py/sysetup)
![PyPI downloads](https://img.shields.io/pypi/dm/sysetup)
![Python version](https://img.shields.io/badge/python-3.10+-brightgreen)
![Operating system](https://img.shields.io/badge/os-linux-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-66%25-brightgreen)
## [Plasma](https://kde.org/plasma-desktop/) 6 required

[Setup info](docs/setup-plasma.md)

## Setup steps
1) Run
   ```shell
   wget -O - sysetup.quintenroets.com | bash
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
    * Click experimental: enable tab groups save and sync
5) Login to
    * Pycharm professional
6) For new device: set touchpad scroll direction and click on touch

## Installation
```shell
pip install sysetup
```
