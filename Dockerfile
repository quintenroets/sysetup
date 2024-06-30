# Base image can be invent-registry.kde.org/neon/docker-images/plasma:latest as well
ARG BASE_IMAGE=python3.12:latest
FROM $BASE_IMAGE

# install the dependencies that are assumed to be present in a fresh OS install
RUN apt-get update && apt-get install -y wget sudo

RUN apt-get update && apt-get install -y curl
RUN curl https://rclone.org/install.sh | sudo bash # temp speedup

# Setup new user
ARG USERNAME=quinten
RUN sudo useradd $USERNAME
RUN sudo echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" | sudo tee -a /etc/sudoers
RUN sudo mkdir -p /home/$USERNAME
RUN sudo chown -R $USERNAME:$USERNAME /home/$USERNAME
ENV HOME=/home/$USERNAME
WORKDIR /home/$USERNAME
USER $USERNAME

# install sysetup
RUN sudo apt install -y python3-venv
RUN python3 -m venv "$HOME/.local/share/envs/qenv"
ENV PATH="/home/quinten/.local/share/envs/qenv/bin:$PATH"
RUN python -m pip install sysetup

COPY . sysetup
RUN sudo chown -R $USERNAME:$USERNAME /home/$USERNAME
RUN python -m pip install --no-deps -e sysetup
