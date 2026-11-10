#! /bin/bash

# Define image name
CONTAINER_NAME=broker
IMAGE_NAME='apache/kafka'
TAG='latest'

# Print header
echo -----------------------------------------------
echo 'Docker image execution script for' $IMAGE_NAME

# Detect processor architecture (from name)
#PROCESSOR_NAME=$(uname -m)
#case "$PROCESSOR_NAME" in 
#  *'arm64'*)
#  TAG=$VERSION'-arm64'
#    ;;
#  *'armv7l'*)
#  TAG=$VERSION'-armhf'
#    ;;
#  *'x86_64'*)
#  TAG=$VERSION'-amd64'
#    ;;
#  *)
 # echo 'Processor architecture' $PROCESSOR_NAME 'not supported, unable to build image'
 # exit 1
#  ;;
#esac


# Check whether the container exists (running or stopped)
echo 'Checking for running containers called ' $CONTAINER_NAME
if docker container inspect "$CONTAINER_NAME" >/dev/null 2>&1; then
    echo "Container '$CONTAINER_NAME' exists."

    # Stop the container if it is running
    if [ "$(docker inspect -f '{{.State.Running}}' "$CONTAINER_NAME")" = "true" ]; then
        echo "Stopping container '$CONTAINER_NAME'..."
        docker stop "$CONTAINER_NAME" || exit 1
    fi

    # Remove the container
    echo "Removing container '$CONTAINER_NAME'..."
    docker rm "$CONTAINER_NAME" || exit 1
    echo "Container '$CONTAINER_NAME' removed."
else
    echo "Container '$CONTAINER_NAME' does not exist."
fi

# Run container
echo 'Running' $TAG 'image'
docker run --name $CONTAINER_NAME \
	-p 9092:9092 \
	-d $IMAGE_NAME:$TAG

# Print footer
echo Done

# End of script
