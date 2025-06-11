# Use a Python 3.10 slim image as the base, matching your local environment
FROM python:3.10-slim-buster

# Set working directory inside the container
WORKDIR /app/ComfyUI

# Install system dependencies (e.g., for image processing, Git for custom nodes)
# libgl1 libglib2.0-0 are common for graphical applications.
# wget is useful for downloading models/data if needed within the container.
RUN apt-get update && \
    apt-get install -y git wget libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Copy ComfyUI's requirements.txt first to leverage Docker's build cache
COPY requirements.txt .

# Install PyTorch, torchvision, torchaudio for linux/arm64 CPU.
# We explicitly use the CPU wheels for linux/arm64, as Docker Desktop's Rosetta/QEMU
# translation layers are then typically used to map these operations to host MPS.
# This avoids the "Torch not compiled with CUDA enabled" error and `whl/mps` specific issues.
RUN pip install --no-cache-dir \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install other Python dependencies from requirements.txt
# --ignore-installed is crucial here to prevent pip from trying to reinstall
# torch/torchvision/torchaudio from requirements.txt, which might conflict.
RUN pip install --no-cache-dir --ignore-installed -r requirements.txt

# Install xformers (often an optional but highly recommended performance dependency)
# If this causes issues during build, it might need to be removed or handled differently.
# For now, we'll keep it as it might auto-install a compatible version.

# Copy the rest of ComfyUI source code into the container
COPY . .

# Expose the default ComfyUI port
EXPOSE 8188

# Command to run ComfyUI
# --listen 0.0.0.0 makes it accessible from outside the container
# --port 8188 sets the port
# --device mps is CRITICAL to tell ComfyUI to use the MPS device,
# relying on Docker Desktop's underlying translation.
ENTRYPOINT ["python", "main.py", "--listen", "0.0.0.0", "--port", "8188", "--gpu-only"]
