from setuptools import setup, find_packages

NAME = "sysetup"

def read(filename):
    try:
        with open(filename) as fp:
            content = fp.read().split("\n")
    except FileNotFoundError:
        content = []
    return content


setup(
    author="Quinten Roets",
    author_email="quinten.roets@gmail.com",
    description='',
    name=NAME,
    version='1.0',
    packages=find_packages(),
    install_requires=read("requirements.txt"),
    entry_points={
        "console_scripts": [
            f"{NAME} = {NAME}.main:main",
            f"exportcrontab = {NAME}.files:move_crontab",
        ]
    },
)
