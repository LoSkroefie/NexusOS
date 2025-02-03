#!/bin/bash

# Build NexusOS Linux Distribution ISO
# This script uses Docker to create the ISO in a controlled environment

set -e

# Configuration
DOCKER_IMAGE="nexusos-builder"
ISO_OUTPUT_DIR="$(pwd)/iso"

# Ensure output directory exists
mkdir -p "${ISO_OUTPUT_DIR}"

# Build Docker image
echo "Building Docker image..."
docker build -t "${DOCKER_IMAGE}" linux/

# Run build process
echo "Building NexusOS ISO..."
docker run --privileged \
    -v "${ISO_OUTPUT_DIR}:/output" \
    -v "$(pwd)/src:/nexusos/src" \
    -v "$(pwd)/requirements.txt:/nexusos/requirements.txt" \
    "${DOCKER_IMAGE}"

echo "ISO build complete! Check the ./iso directory for your NexusOS ISO."
