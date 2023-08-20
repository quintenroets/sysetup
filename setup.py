from pathlib import Path

from setuptools import find_packages, setup

NAME = "sysetup"


def read(filename):
    try:
        with open(filename) as fp:
            content = fp.read().split("\n")
    except FileNotFoundError:
        content = []
    return content


package_folder = Path(__file__).parent
shell_scripts = [
    str(p.relative_to(package_folder)) for p in package_folder.glob("bin/*")
]


setup(
    author="Quinten Roets",
    author_email="quinten.roets@gmail.com",
    description="",
    name=NAME,
    version="1.0.0",
    packages=find_packages(),
    install_requires=read("requirements.txt"),
    scripts=shell_scripts,
    entry_points={
        "console_scripts": [
            f"{NAME} = {NAME}.main:main",
            f"exportcrontab = {NAME}.files:move_crontab",
        ]
    },
)
