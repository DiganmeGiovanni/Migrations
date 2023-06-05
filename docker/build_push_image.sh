#!/bin/bash
#
# Builds and pushes a new 'mat' multiarch docker image
# Image tag is specified by first argument:
# > ./build_push_image.sh 1.0.2
#

IMAGE_TAG=0

if [ "$1" = "" ]; then
  echo "Image tag should be specified as argument"
  exit 1
else
  IMAGE_TAG=$1
fi

if ! [ -f "./mat.docker" ]; then
  echo "Docker file not found './mat.docker'"
  exit 1
fi

docker buildx build                    \
    --platform linux/amd64,linux/arm64 \
    -t giobyte8/mat:"$IMAGE_TAG"       \
    -f mat.docker                      \
    --push                             \
    .

echo
echo "Verion $IMAGE_TAG of 'mat' was released to docker registry"
