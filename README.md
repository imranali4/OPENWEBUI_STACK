cat << EOF > README.md
# OPENWEBUI_STACK - Comprehensive AI & Automation Stack
  
This repository contains a full AI and automation stack orchestrated with Docker Compose, featuring:
  
- Open WebUI: A user-friendly interface for your LLM interactions.
- BAAI/bge-reranker-v2-m3: A powerful hybrid reranker for improved search relevance.
- SearXNG: A privacy-respecting metasearch engine.
- Tika: For content extraction.
- TTS Piper: For text-to-speech capabilities.
- n8n: A powerful workflow automation tool to connect APIs and automate tasks.
- Cloudflare Tunnel: For exposing services securely.
- ComfyUI: A modular and powerful Stable Diffusion UI for image generation.
  
This stack is designed to be easily deployed by users with Docker Desktop.
  
## Getting Started
  
Follow these concise steps to set up and run the full AI and automation stack on your machine.
  
### Prerequisites
  
- **Docker Desktop:** Ensure Docker Desktop is installed and running. ([Download](https://www.docker.com/products/docker-desktop/))
- **Git:** You'll need Git installed to clone this repository. ([Download](https://git-scm.com/downloads))
  
### Repository Contents Overview
  
Your cloned \`OPENWEBUI_STACK\` directory contains the \`docker-compose.yml\` and associated local code/configurations:
  
- \`docker-compose.yml\` (Main orchestration file for all services)
- \`ComfyUI/\` (Local source for ComfyUI service)
- \`hybridreranker/\` (Local source for Hybrid Reranker service)
- \`my_custom_tools/\` (Custom tool scripts for Open WebUI)
- \`openedai-speech/\` (Config and voice models for TTS Piper)
- \`searxng-docker/\` (Configuration for SearXNG)
- \`.env.example\` (Template for environment variables)
- \`.gitignore\` (Files/folders Git ignores)
- \`README.md\` (This guide!)
  
### The Deployed Stack: Services Orchestrated by \`docker-compose.yml\`
  
This table directly reflects the services that will be running, their source, and purpose:
  
| Service Name (as in Docker Desktop) | Image / Source                        | Description                                          |
| :---------------------------------- | :------------------------------------ | :--------------------------------------------------- |
| \`open-webui\`                      | \`ghcr.io/open-webui/open-webui:latest\`| User interface for LLM interactions.                 |
| \`searxng-caddy\`                   | \`caddy:2-alpine\`                    | Reverse proxy for SearXNG.                           |
| \`searxng\`                         | \`searxng/searxng:latest\`            | Privacy-respecting metasearch engine.                |
| \`n8n\`                             | \`n8nio/n8n:latest\`                  | Powerful workflow automation tool.                   |
| \`openedai-speech\`                 | \`ghcr.io/matatonic/openedai-speech-min:latest\` | Text-to-Speech service.                              |
| \`hybridreranker\`                  | Built from \`./hybridreranker\`       | Improves search relevance with custom logic.         |
| \`cloudflared-tunnel\`              | \`cloudflare/cloudflared:latest\`     | Secure tunnel for exposing services (configured via .env). |
| \`tika\`                            | \`apache/tika:latest-full\`           | Content extraction service.                          |
| \`searxng-redis\`                   | \`valkey/valkey:8-alpine\`            | Redis backend for SearXNG.                           |
| \`comfyui\`                         | Built from \`./ComfyUI\`              | Modular UI for Stable Diffusion image generation.    |
  
### Step 1: Clone the Project
  
1.  Open your terminal or command prompt.
2.  Clone this repository:
    \`\`\`bash
    git clone https://github.com/imranali4/OPENWEBUI_STACK.git
    \`\`\`
3.  Navigate into the cloned project directory:
    \`\`\`bash
    cd OPENWEBUI_STACK
    \`\`\`
  
### Step 2: Configure Environment Variables (API Keys & Tokens)
  
Some services require API keys/tokens.
  
1.  In the \`OPENWEBUI_STACK\` directory, create a new file named \`.env\` by copying the example:
    \`\`\`bash
    cp .env.example .env
    \`\`\`
2.  Open the newly created \`.env\` file in a text editor and add your API keys and tokens:
    \`\`\`
    OPENAI_API_KEY=sk-your-actual-openai-api-key-here
    CLOUDFLARED_TOKEN=your_actual_cloudflare_tunnel_token_here
    \`\`\`
    **Important:** Replace \`sk-your-actual-openai-api-key-here\` and \`your_actual_cloudflare_tunnel_token_here\` with your real keys.
    **Security Note:** The \`.env\` file is excluded from Git by \`.gitignore\`, so your sensitive information remains local.
  
### Step 3: Prepare ComfyUI Data (Important!)
  
ComfyUI requires large models (e.g., Stable Diffusion checkpoints, Loras, VAEs, Upscalers) which are not included in this Git repository due to their size. You will need to download these models separately and place them in the correct local folders.
  
1.  Ensure required ComfyUI data directories exist on your host. Docker Compose will create empty \`models\`, \`output\`, \`input\`, and \`custom_nodes\` directories if they don't exist, but it's good practice to ensure they're there for manual placement:
    \`\`\`bash
    mkdir -p ComfyUI/models/checkpoints # For main models
    mkdir -p ComfyUI/models/loras
    mkdir -p ComfyUI/models/vae
    mkdir -p ComfyUI/models/upscale_models
    mkdir -p ComfyUI/output
    mkdir -p ComfyUI/input
    mkdir -p ComfyUI/custom_nodes # For any custom nodes you download
    \`\`\`
2.  **Download your desired Stable Diffusion models:**
    For example, you can download \`sd_xl_base_1.0.safetensors\` from Hugging Face: https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/main/sd_xl_base_1.0.safetensors
3.  Place your downloaded checkpoint files (e.g., \`.safetensors\`, \`.ckpt\`) into: \`OPENWEBUI_STACK/ComfyUI/models/checkpoints/\`
4.  Place other model types (e.g., Loras, VAEs, Upscalers) into their respective subdirectories under \`OPENWEBUI_STACK/ComfyUI/models/\`. (ComfyUI typically looks for these automatically).
  
### Step 4: Run the Full Stack
  
This command will build any necessary custom images, download external models (like the reranker model from Hugging Face), and start all the services defined in \`docker-compose.yml\`.
  
1.  Make sure you are in the \`OPENWEBUI_STACK\` directory in your terminal.
2.  Execute the following command:
    \`\`\`bash
    docker compose up --build -d
    \`\`\`
    - \`up\`: Starts the services.
    - \`--build\`: This is crucial! It tells Docker Compose to build your custom \`hybridreranker\` and \`comfyui\` images before starting the containers.
    - \`-d\`: Runs the containers in "detached" mode.
3.  Allow time for Docker to download/build everything.
  
### Step 5: Access & Integrate Services
  
Once services are up, here's how to access them and ensure Open WebUI is fully linked:
  
- **Open WebUI:** Go to [http://localhost:3000](http://localhost:3000).
  - **LLM Integration (e.g., LM Studio):** Open WebUI is configured to connect to an LLM at \`http://host.docker.internal:1234/v1\`. You'll need a compatible LLM server (like LM Studio or Ollama) running on your Docker host on port 1234.
  - **N8N Pipeline Integration:** To enable the "n8n Pipeline" function in Open WebUI, you need to *import* the workflow JSON.
    1.  Access your n8n UI at [http://localhost:5678](http://localhost:5678) (create user on first access).
    2.  In Open WebUI, navigate to **Settings (gear icon) > Functions**.
    3.  Click "Import Functions" and provide the URL to the N8N workflow template: \`https://github.com/owndev/Open-WebUI-Functions/blob/master/pipelines/n8n/Open_WebUI_Test_Agent.json\`
    4.  Configure the function within Open WebUI settings as needed.
  - **Search/RAG Integrations (SearXNG, Tika, Hybrid Reranker):** These services are automatically networked with Open WebUI by \`docker-compose.yml\`. You'll configure their usage within Open WebUI's settings (e.g., RAG settings, search engine URL in Open WebUI environment variables).
  
- **ComfyUI (Stable Diffusion UI):** Go to [http://localhost:8188](http://localhost:8188).
  - **Integration with Open WebUI:** In Open WebUI, go to **Settings > Image Generation (Experimental)**. Set Engine to ComfyUI, and Base URL to \`http://comfyui:8188\`. You'll need to upload a \`workflow.json\` (API format) via the "ComfyUI Workflow" section. Export an example from ComfyUI itself.
  
- **SearXNG Search Engine:** Go to [http://localhost:8080](http://localhost:8080).
- **Tika (Content Extraction):** (Primarily internal) [http://localhost:9998](http://localhost:9998).
- **Hybrid Reranker:** (Primarily internal) [http://localhost:8999](http://localhost:8999).
- **TTS Piper (Text-to-Speech):** (Primarily internal) [http://localhost:8000](http://localhost:8000).
- **n8n (Workflow Automation):** Go to [http://localhost:5678](http://localhost:5678).
- **Cloudflare Tunnel:** Configured via your \`.env\` file for secure external access.
  
### Step 6: Stop the Services
  
1.  Navigate to \`OPENWEBUI_STACK\` directory.
2.  Run: \`docker compose down\`
  
### Step 7: Clean Up (Optional: Delete all data and images)
  
1.  Navigate to \`OPENWEBUI_STACK\` directory.
2.  Run: \`docker compose down --volumes --rmi local\`
    - \`--volumes\`: Removes named Docker volumes (deletes persistent data).
    - \`--rmi local\`: Removes locally built images.
EOF