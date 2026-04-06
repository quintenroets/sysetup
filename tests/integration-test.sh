#!/bin/bash
set -eo pipefail
qemu_noise='^<jemalloc>:|^head:.*proc/self/exe|^ERROR: unknown platform bitness|^sh: [0-9]*: \[: Illegal number'

BW_CLIENTID="${BW_CLIENTID:-$(pw bitwarden_client_id)}"
BW_CLIENTSECRET="${BW_CLIENTSECRET:-$(pw bitwarden_client_secret)}"
BITWARDEN="${BITWARDEN:-$(pw bitwarden_master_password)}"

if [ -z "${IMAGE_TAG:-}" ]; then
    IMAGE_TAG="sysetup"
    DOCKER_BUILDKIT=1 docker build --platform linux/amd64 -t "$IMAGE_TAG" -f tests/Dockerfile .
fi

docker run --platform linux/amd64 \
    -e BW_CLIENTID="$BW_CLIENTID" \
    -e BW_CLIENTSECRET="$BW_CLIENTSECRET" \
    "$IMAGE_TAG" "$BITWARDEN" \
    2>&1 | grep -Ev "$qemu_noise"
