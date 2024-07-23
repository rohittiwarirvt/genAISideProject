#!/bin/bash

set -eu



echo "-------------------------------------------------------------------------------"
echo "Building docker image for frontend."
echo "-------------------------------------------------------------------------------"

set +xe

source ./build-env.sh

NEXT_PUBLIC_GENAIBACKEND=${NEXT_PUBLIC_GENAIBACKEND}
NEXT_PUBLIC_IS_MOCKEDLLM=${NEXT_PUBLIC_IS_MOCKEDLLM}

# just placeholder not needed though
# Still needs implementaion
NEXTAUTH_URL=${NEXTAUTH_URL}
# Next Auth Discord Provider
DISCORD_CLIENT_ID=${DISCORD_CLIENT_ID}
DISCORD_CLIENT_SECRET=${DISCORD_CLIENT_SECRET}

docker build -t ct3a-docker  \
  --build-arg NEXT_PUBLIC_IS_MOCKEDLLM=${NEXT_PUBLIC_IS_MOCKEDLLM} \
  --build-arg NEXT_PUBLIC_GENAIBACKEND=${NEXT_PUBLIC_GENAIBACKEND} \
  --build-arg NEXTAUTH_URL=${NEXTAUTH_URL} \
  --build-arg DISCORD_CLIENT_ID=${DISCORD_CLIENT_ID} \
  --build-arg DISCORD_CLIENT_SECRET=${DISCORD_CLIENT_SECRET} . \

