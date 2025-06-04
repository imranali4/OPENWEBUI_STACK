# Use a suitable base image for ComfyUI
FROM python:3.10-slim-buster

# Set working directory inside the container
WORKDIR /app/ComfyUI

# Install system dependencies (e.g., for image processing, Git for custom nodes)
# libgl1 and libglib2.0-0 are common for graphical applications.
# wget is useful for downloading models/data if needed within the container.
RUN apt-get update && \
    apt-get install -y git wget libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Copy ComfyUI's requirements.txt first to leverage Docker's build cache
# If requirements.txt changes, only the pip install layers are rebuilt.
COPY requirements.txt .

# Install PyTorch and related core libraries first due to size and specific installation methods.
# This example uses CPU-only PyTorch (suitable for most Mac users without NVIDIA GPUs).
# If you intend to leverage Apple Silicon (MPS) for acceleration, change the --index-url to:
# https://download.pytorch.org/whl/mps
RUN pip install --no-cache-dir \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install other Python dependencies from requirements.txt
# This will install libraries like transformers, safetensors, numpy, etc.
# Note: If 'comfyui-frontend-package' or 'comfyui-workflow-templates' are not public PyPI
# packages, pip might warn or skip them. They are likely handled by the 'COPY . .' step.
RUN pip install --no-cache-dir -r requirements.txt

# Install xformers (often an optional but good performance dependency, especially for stable diffusion)
# This is often needed by ComfyUI.
RUN pip install --no-cache-dir xformers

# Copy the rest of ComfyUI source code into the image
# This comes after dependency installation to optimize caching:
# If only your application code changes, this layer and subsequent layers are rebuilt,
# but the large dependency layers (including PyTorch) are reused.
COPY . .

# Expose the default ComfyUI port
EXPOSE 8188

# Command to run ComfyUI
# --listen 0.0.0.0 makes it accessible from outside the container
# --port 8188 sets the port
ENTRYPOINT ["python", "main.py", "--listen", "0.0.0.0", "--port", "8188"]