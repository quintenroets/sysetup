#!/bin/bash
set -o pipefail
qemu_noise='^<jemalloc>:|^head:.*proc/self/exe|^ERROR: unknown platform bitness|^sh: [0-9]*: \[: Illegal number'

DOCKER_BUILDKIT=1 docker build --platform linux/amd64 -t sysetup -f tests/Dockerfile . &&
    docker run --platform linux/amd64 \
        -e BW_CLIENTID="$(pw bitwarden_client_id)" \
        -e BW_CLIENTSECRET="$(pw bitwarden_client_secret)" \
        sysetup "$(pw bitwarden_master_password)" \
        2>&1 | grep -Ev "$qemu_noise"
