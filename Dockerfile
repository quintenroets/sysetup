FROM python:3.11

ARG USERNAME=quinten

ENV oer=ar

RUN apt-get update && apt-get install -y wget sudo

RUN useradd $USERNAME

RUN echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN mkdir -p /home/$USERNAME

RUN chown -R $USERNAME:$USERNAME /home/$USERNAME

USER $USERNAME

RUN sudo apt install -y python3.11-venv

RUN python3 -m venv "$HOME/.local/share/envs/qenv"

RUN "$HOME/.local/share/envs/qenv/bin/python" -m pip install --upgrade git+https://github.com/quintenroets/sysetup@fix-setup

# RUN pip install git+https://github.com/quintenroets/backup.git@debug

ENV PATH="$PATH:/home/quinten/.local/share/envs/qenv/bin"
