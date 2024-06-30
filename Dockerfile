# Base image can be invent-registry.kde.org/neon/docker-images/plasma:latest as well
ARG BASE_IMAGE=python:3.12
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

ENV OER=ar
RUN wget -O setup.sh https://raw.githubusercontent.com/quintenroets/sysetup/fix-setup/bin/setup
RUN chmod +x setup.sh

ENTRYPOINT ["./setup.sh"]
