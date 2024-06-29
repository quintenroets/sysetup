#! /bin/bash

env_name="qenv"
venv_path="$HOME/.local/share/envs/$env_name"

if [ ! -d "$venv_path" ]; then
    sudo apt install -y python3.11-venv
    python3 -m venv "$venv_path"
fi

source "$venv_path/bin/activate"
python -m pip install --upgrade git+https://github.com/quintenroets/sysetup@fix-setup
