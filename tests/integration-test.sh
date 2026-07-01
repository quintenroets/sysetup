#!/bin/bash
set -eo pipefail
qemu_noise='^<jemalloc>:|^head:.*proc/self/exe|^ERROR: unknown platform bitness|^sh: [0-9]*: \[: Illegal number'

if [ -z "${IMAGE_TAG:-}" ]; then
    IMAGE_TAG="sysetup"
    DOCKER_BUILDKIT=1 docker build --platform linux/amd64 -t "$IMAGE_TAG" -f tests/Dockerfile .
fi

docker run --platform linux/amd64 \
    -e BW_CLIENTID="${BW_CLIENTID:-$($SECRET_ASKPASS bitwarden_client_id)}" \
    -e BW_CLIENTSECRET="${BW_CLIENTSECRET:-$($SECRET_ASKPASS bitwarden_client_secret)}" \
    -e BITWARDEN="${BITWARDEN:-$($SECRET_ASKPASS bitwarden_master_password)}" \
    "$IMAGE_TAG" \
    2>&1 | grep -Ev "$qemu_noise"
