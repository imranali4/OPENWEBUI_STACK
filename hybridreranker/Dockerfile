# Use a slim Python 3.10 image as the base
FROM python:3.10-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (like curl, useful for general HTTP requests, though not strictly needed for transformers download)
# We remove git-lfs because we are no longer tracking large files directly in this image
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies:
# - torch and torchvision (with MPS support for Apple Silicon)
# - transformers and accelerate (for loading Hugging Face models)
# - fastapi and uvicorn (your web server)
# - sentence-transformers (often useful for rerankers like BGE)
RUN pip install --no-cache-dir \
      torch torchvision --extra-index-url https://download.pytorch.org/whl/mps \
      transformers accelerate \
      fastapi uvicorn \
      sentence-transformers

# --- Crucial: Pre-download and cache the BAAI/bge-reranker-v2-m3 model during the build ---
# This makes the Docker image larger but ensures the model is present when the container starts,
# avoiding runtime downloads and potential network issues.
# Set an environment variable for Hugging Face cache directory within the container
ENV HF_HOME=/app/huggingface_cache
# Create the directory for the cache
RUN mkdir -p ${HF_HOME}
# Define the model name as a build argument
ARG MODEL_NAME="BAAI/bge-reranker-v2-m3"
# Use a Python command to download the tokenizer and model
RUN python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; \
    print(f'Downloading model: ${MODEL_NAME}'); \
    AutoTokenizer.from_pretrained('${MODEL_NAME}'); \
    AutoModelForSequenceClassification.from_pretrained('${MODEL_NAME}')"

# Copy your application code into the container
# This copies your inference.py and any other local code files
COPY . /app

# Document the port the FastAPI server will listen on
# IMPORTANT: This must match the 'ports' mapping in your docker-compose.yml (which is 8999)
EXPOSE 8999

# Command to launch the FastAPI server
# Make sure your 'inference.py' file defines a FastAPI application object named 'app'
ENTRYPOINT ["uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "8999"]