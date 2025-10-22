#!/bin/bash

# Exit on any error
set -e

# --- CONFIGURATION ---
NAMESPACE_NAME="htalukder-cr"
REGISTRY="us.icr.io"
VERSION="v2"  # Increment manually when needed

# --- HELP MENU ---
usage() {
  echo "Usage: $0 [backend|frontend]"
  echo "Example: $0 backend"
  echo "Example: $0 frontend"
  exit 1
}

# --- VALIDATE INPUT ---
if [ $# -ne 1 ]; then
  usage
fi

TARGET=$1

if [[ "$TARGET" != "backend" && "$TARGET" != "frontend" ]]; then
  echo "Invalid argument: $TARGET"
  usage
fi

# --- DEFINE IMAGE NAME BASED ON TARGET ---
if [ "$TARGET" == "backend" ]; then
  IMAGE_NAME="celery_backend_app" # change the image name
  BUILD_DIR="backend"
elif [ "$TARGET" == "frontend" ]; then
  IMAGE_NAME="celery_frontend_app"
  BUILD_DIR="frontend"
fi

# --- GENERATE IMAGE TAG ---
DAY=$(date +%d)
MONTH=$(date +%m)
YEAR=$(date +%Y)
IMAGE_TAG="${DAY}${MONTH}${YEAR}-${VERSION}"
FULL_IMAGE_NAME="${REGISTRY}/${NAMESPACE_NAME}/${IMAGE_NAME}:${IMAGE_TAG}"

# --- LOGIN TO IBM CLOUD CONTAINER REGISTRY ---
echo "--------------------------------------------------"
echo "Logging in to IBM Cloud Container Registry..."
echo "--------------------------------------------------"
ibmcloud cr login

# --- BUILD IMAGE ---
echo "--------------------------------------------------"
echo "Building image for: ${TARGET}"
echo "Image: ${FULL_IMAGE_NAME}"
echo "--------------------------------------------------"
cd ../../"$BUILD_DIR"

podman build -t "${FULL_IMAGE_NAME}" .

# --- PUSH IMAGE ---
echo "--------------------------------------------------"
echo "Pushing image to IBM Cloud Container Registry..."
echo "--------------------------------------------------"
podman push "${FULL_IMAGE_NAME}"

# --- SUCCESS MESSAGE ---
echo "--------------------------------------------------"
echo "Successfully built and pushed ${TARGET} image!"
echo "Image URL: ${FULL_IMAGE_NAME}"
echo "--------------------------------------------------"
