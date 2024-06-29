FROM python:3.11

ARG USERNAME=quinten

RUN apt-get update && apt-get install -y wget sudo

RUN useradd $USERNAME

RUN echo '$USERNAME ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN mkdir -p /home/$USERNAME

RUN chown -R $USERNAME:$USERNAME /home/$USERNAME

USER $USERNAME

COPY setup.sh .

RUN bash setup.sh

# RUN pip install git+https://github.com/quintenroets/backup.git@debug

ENV PATH="$PATH:/home/quinten/.local/share/envs/qenv/bin"
