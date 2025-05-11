#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Line 1: Pull the latest image. The tag is fetched by executing pull_latest.py.
docker pull "ghcr.io/mgetf/tf2-ladder/i386:$(./pull_latest.py)"

# Line 2: Force remove the existing container. Replace 'tf2_ladder_service' if your container has a different name.
# The '|| true' ensures the script doesn't exit if the container isn't found (e.g., on first run).
docker rm -f tf2_ladder_service || true

# Line 3: Run the new container. 
# IMPORTANT: Replace 'tf2_ladder_service' with your container's desired name.
# IMPORTANT: Replace 'YOUR_DOCKER_RUN_OPTIONS_HERE' with your actual Docker run command options 
# (e.g., -d --network=host -e RCON_PASSWORD=your_pass --restart always).
# The tag is fetched again by executing pull_latest.py.
docker run --name tf2_ladder_service --pull=always --network=host -e RCON_PASSWORD=123456 -e SERVER_PASSWORD=mgeisfun -itd "ghcr.io/mgetf/tf2-ladder/i386:$(./pull_latest.py)"

echo "Update process initiated. If successful, the new container should be running." 
docker ps