#!/bin/bash
VERSION=$(cat version.txt)
echo "Building Docker image diploma-rest:${VERSION}..."
docker build -f Dockerfile.dev -t diploma-rest:${VERSION} .

echo "Checking for existing container..."
if [ "$(docker ps -a -q -f name=diploma-rest)" ]; then
    echo "Stopping and removing existing container..."
    docker stop diploma-rest
    docker rm diploma-rest
fi

echo "Starting new container..."
docker run -d -p 8000:8000 --name diploma-rest diploma-rest:${VERSION}

echo "Container status:"
docker ps | grep diploma-rest