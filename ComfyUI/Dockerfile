# Use a Python 3.10 slim image as the base, matching your local environment
FROM python:3.10-slim-buster

# Set working directory inside the container
WORKDIR /app/ComfyUI

# Install system dependencies
# git: for cloning custom nodes if users add them.
# wget: useful for downloading models/checkpoints later if chosen by user.
# libgl1 libglib2.0-0: common for graphical applications like ComfyUI.
RUN apt-get update && \
    apt-get install -y git wget libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Copy ComfyUI's requirements.txt first to leverage Docker's build cache
# If requirements.txt changes, only the pip install layers are rebuilt.
COPY requirements.txt .

# Install PyTorch, torchvision, torchaudio with MPS (Metal) support for Apple Silicon.
# This is critical for leveraging your M1's GPU.
# Confirmed PyTorch version 2.7.0 from your pip list.
RUN pip install --no-cache-dir \
    torch==2.7.0 torchvision==0.22.0 torchaudio==2.7.0 --index-url https://download.pytorch.org/whl/mps

# Install other Python dependencies from requirements.txt
# (Excludes torch/torchvision/torchaudio as they are installed above)
# The --ignore-installed is crucial here to prevent pip from trying to reinstall
# torch/torchvision/torchaudio from requirements.txt, which might mess with MPS.
RUN pip install --no-cache-dir --ignore-installed -r requirements.txt

# Install xformers (often an optional but highly recommended performance dependency for stable diffusion)
# Check if xformers has an MPS wheel, if not, CPU will be used or it might fail if not compatible.
# For now, we'll try a generic installation.
RUN pip install --no-cache-dir xformers

# Copy the rest of ComfyUI source code into the container
# This comes after dependency installation to optimize caching:
# If only your application code changes, this layer and subsequent layers are rebuilt,
# but the large dependency layers (including PyTorch) are reused.
COPY . .

# Expose the default ComfyUI port
EXPOSE 8188

# Command to run ComfyUI
# --listen 0.0.0.0 makes it accessible from outside the container
# --port 8188 sets the port
# You might want to add --device mps or --enable-mps-fallback to main.py args
# to explicitly tell ComfyUI to use MPS, although it often auto-detects.
ENTRYPOINT ["python", "main.py", "--listen", "0.0.0.0", "--port", "8188"]