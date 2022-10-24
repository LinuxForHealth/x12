#!/bin/bash
# push-image.sh
# push-image.sh builds and pushes the multi-platform linuxforhealth/x12 image to an image repository.
#
# Pre-Requisites:
# - The script environment is authenticated to the target image repository.
# - The project has been built and a wheel exists in <project root>/dist.
#
# Usage:
# ./push-image [image_tag] [image_url] [platforms]
#
# Positional Script arguments:
# IMAGE_TAG - Aligns with the project's semantic version. Required.
# IMAGE_URL - The image's URL. Defaults to ghcr.io/linuxforhealth/x12.
# PLATFORMS - String containing the list of platforms. Defaults to linux/amd64,linux/arm64,linux/s390x.

set -o errexit
set -o nounset
set -o pipefail

if [[ $# == 0 ]]
  then
    echo "Missing required argument IMAGE_TAG"
    echo "Usage: ./push-image.sh [image tag] [image url] [platforms]"
    exit 1;
fi

IMAGE_TAG=$1
IMAGE_URL="${2:-ghcr.io/linuxforhealth/x12}"
PLATFORMS="${3:-linux/amd64,linux/arm64}"

docker buildx build \
              --pull \
              --push \
              --platform "$PLATFORMS" \
              --build-arg X12_SEM_VER="$IMAGE_TAG" \
              --tag "$IMAGE_URL":"$IMAGE_TAG" \
              --tag "$IMAGE_URL":latest .
