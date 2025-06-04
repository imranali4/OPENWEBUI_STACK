#!/bin/bash

# This script activates the ComfyUI conda environment and starts the ComfyUI server.
# It assumes your ComfyUI installation is at /Users/imranali/projects/comfyui/ComfyUI
# and your Miniconda3 installation is at /Users/imranali/miniconda3

# Define the absolute path to your ComfyUI installation
COMFYUI_DIR="/Users/imranali/projects/comfyui/ComfyUI"

# Define the absolute path to your Miniconda3 installation
MINICONDA_PATH="/Users/imranali/miniconda3"

echo "Navigating to ComfyUI directory..."
cd "$COMFYUI_DIR" || { echo "Error: Could not change to ComfyUI directory."; exit 1; }

echo "Activating comfyui conda environment..."
# Initialize conda for the current shell session
# This ensures 'conda activate' works in the script
source "$MINICONDA_PATH/etc/profile.d/conda.sh"

# Activate the comfyui conda environment
conda activate comfyui || { echo "Error: Could not activate comfyui conda environment. Does it exist?"; exit 1; }

echo "Starting ComfyUI server..."
python main.py --listen 0.0.0.0 --port 8188

echo "ComfyUI server stopped."
