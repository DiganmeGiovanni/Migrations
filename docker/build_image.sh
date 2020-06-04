#!/bin/bash
#
# Builds a new 'mat' docker image
# Image tag is specified by first argument
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

docker build -t mat:"$IMAGE_TAG" -f mat.docker .
