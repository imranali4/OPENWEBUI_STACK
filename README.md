# OPENWEBUI_STACK - Comprehensive AI & Automation Stack

This repository contains a full AI and automation stack orchestrated with Docker Compose, featuring:
*   **Open WebUI:** A user-friendly interface for your LLM interactions.
*   **BAAI/bge-reranker-v2-m3:** A powerful hybrid reranker for improved search relevance.
*   **SearXNG:** A privacy-respecting metasearch engine.
*   **Tika:** For content extraction.
*   **TTS Piper:** For text-to-speech capabilities.
*   **n8n:** A powerful workflow automation tool to connect APIs and automate tasks.
*   **ComfyUI:** A modular and powerful Stable Diffusion UI for image generation.

This stack is designed to be easily deployed by users with Docker Desktop.

---

## Getting Started

Follow these steps to set up and run the full AI and automation stack on your machine.

### Prerequisites

*   **Docker Desktop:** Ensure Docker Desktop is installed and running on your Windows, macOS, or Linux machine.
    *   Download from: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
*   **Git:** You'll need Git installed to clone this repository.
    *   Download from: [https://git-scm.com/downloads](https://git-scm.com/downloads)

### Project Structure

After cloning, your project directory (`OPENWEBUI_STACK`) will have the following structure:
```
OPENWEBUI_STACK/ 
├── docker-compose.yml # The main Docker Compose orchestration file 
├── hybridreranker/ # Contains Dockerfile and code for the custom reranker 
 │ ├── Dockerfile 
 │ ├── inference.py 
 │ └── requirements.txt 
├── my_custom_tools/ # Custom tool scripts for Open WebUI 
 │ └── example_tool.py 
├── openedai-speech/ # Configuration and voice models for TTS Piper 
 │ ├── config/ 
 │ └── voices/ 
├── searxng-docker/ # Configuration for SearXNG 
 │ └── searxng/ 
 │ └── settings.yml 
├── .env.example # Template for environment variables (e.g., API keys) 
├── .gitignore # Specifies files/folders Git should ignore 
├── comfyui/ # ComfyUI source code (model/output/input/custom_nodes ignored by Git) 
 │ ├── Dockerfile 
 │ ├── requirements.txt 
 │ └── ... (ComfyUI core files) 
└── README.md # This guide!
```

---

### Step 1: Clone the Project

1.  Open your terminal or command prompt.
2.  Clone this repository:
    ```bash
    git clone https://github.com/imranali4/OPENWEBUI_STACK.git
    ```
3.  Navigate into the cloned project directory:
    ```bash
    cd OPENWEBUI_STACK
    ```

### Step 2: Configure Environment Variables (API Key)

Some services require API keys. The `OPENAI_API_KEY` is used by Open WebUI.

1.  In the `OPENWEBUI_STACK` directory, create a new file named `.env` by copying the example:
    ```bash
    cp .env.example .env
    ```
2.  Open the newly created `.env` file in a text editor and add your `OPENAI_API_KEY`:
    ```dotenv
    OPENAI_API_KEY=sk-your-actual-openai-api-key-here
    ```
    **Important:** Replace `sk-your-actual-openai-api-key-here` with your real OpenAI API key.
    *   **Security Note:** The `.env` file is excluded from Git by `.gitignore`, so your sensitive information remains local.

### Step 3: Prepare ComfyUI Data (Important!)

ComfyUI requires large models (e.g., Stable Diffusion checkpoints, Loras, VAEs, Upscalers) which are **not included in this Git repository** due to their size. You will need to download these models separately and place them in the correct local folders.

1.  **Ensure required ComfyUI data directories exist on your host:**
    Docker Compose will create these if they don't exist, but it's good practice to ensure they're there.
    ```bash
    mkdir -p comfyui/models
    mkdir -p comfyui/output
    mkdir -p comfyui/input
    mkdir -p comfyui/custom_nodes # For any custom nodes you download
    ```
2.  **Download your desired Stable Diffusion models:**
    *   For example, you can download `sd_xl_base_1.0.safetensors` from Hugging Face: [https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/main/sd_xl_base_1.0.safetensors](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/main/sd_xl_base_1.0.safetensors)
    *   **Place your downloaded checkpoint files** (e.g., `.safetensors`, `.ckpt`) into: `OPENWEBUI_STACK/comfyui/models/checkpoints/`
    *   **Place other model types** (e.g., Loras, VAEs, Upscalers) into their respective subdirectories under `OPENWEBUI_STACK/comfyui/models/`. (ComfyUI typically looks for these automatically).

### Step 4: Run the Full Stack

This command will build any necessary custom images, download external models (like the reranker model from Hugging Face), and start all the services defined in `docker-compose.yml`.

1.  Make sure you are in the `OPENWEBUI_STACK` directory in your terminal.
2.  Execute the following command:
    ```bash
    docker compose up --build -d
    ```
    *   `up`: Starts the services.
    *   `--build`: This is crucial! It tells Docker Compose to build your custom `hybridreranker` and `comfyui` images before starting the containers. During the `comfyui` build, it will install PyTorch with MPS support.
    *   `-d`: Runs the containers in "detached" mode (in the background), so your terminal remains free. If you want to see all logs directly, remove `-d`.

    Allow some time for Docker to download images, build your custom images, and download any required models within the containers.

### Step 5: Access the Services

Once the services are up and running, you can access them via your web browser:

*   **Open WebUI:**
    *   Go to: `http://localhost:3000`
    *   **Note on LLM:** Open WebUI is configured to connect to an LLM running on `http://host.docker.internal:1234/v1`. This assumes you have a compatible LLM (like Ollama or a local LLM server) running on your Docker host machine, serving on port `1234`. If you don't, Open WebUI's AI features won't work immediately.
    *   **ComfyUI Integration (Optional):** This stack includes ComfyUI, but its integration with Open WebUI is not pre-configured via environment variables due to the need for a specific workflow.json file. You can manually set up the connection within Open WebUI settings:
        *   Navigate to **Settings (gear icon) > Image Generation (Experimental)**.
        *   Set **Image Generation Engine** to `ComfyUI`.
        *   For **ComfyUI Base URL**, enter `http://comfyui:8188`
        *   **Important: You must upload a `workflow.json` file as API format** via the "ComfyUI Workflow" section. You can export an example workflow from ComfyUI itself (e.g., from `http://localhost:8188`) by selecting `Save (API Format)` from the `Save` menu.
        *   Once a workflow is uploaded, you can then configure the specific node IDs and parameters (Prompt, Model, Width, Height, etc.) directly in Open WebUI's settings.
*   **SearXNG Search Engine (via Caddy proxy):**
    *   Go to: `http://localhost:8080`
*   **Tika (Content Extraction):** (Primarily for internal use by Open WebUI if configured for RAG)
    *   Accessible at: `http://localhost:9998`
*   **Hybrid Reranker:** (Primarily for internal use)
    *   Accessible at: `http://localhost:8999`
*   **TTS Piper (Text-to-Speech):** (Primarily for internal use)
    *   Accessible at: `http://localhost:8000`
*   **n8n (Workflow Automation):**
    *   Go to: `http://localhost:5678`
    *   On first access, n8n will guide you through creating your first user account. This account will be persistent in the `n8n_data` Docker volume.
*   **ComfyUI (Stable Diffusion UI):**
    *   Go to: `http://localhost:8188`
    *   You can directly access ComfyUI's web interface here to load workflows, generate images, and manage models.

### Step 6: Stop the Services

When you're done, you can stop all running containers:

*   Navigate back to the `OPENWEBUI_STACK` directory in your terminal.
*   Run:
    ```bash
    docker compose down
    ```
    This will stop and remove the containers and networks. **Your data (e.g., Open WebUI database, SearXNG data, n8n workflows, ComfyUI output) stored in Docker volumes and bind mounts will be preserved.**

### Step 7: Clean Up (Optional: Delete all data and images)

If you want to completely remove all data, containers, networks, and locally built images, use this command:

*   Navigate back to the `OPENWEBUI_STACK` directory in your terminal.
*   Run:
    ```bash
    docker compose down --volumes --rmi local
    ```
    *   `--volumes` (or `-v`): Removes the named Docker volumes, which store your persistent data. **This will delete your data.**
    *   `--rmi local`: Removes images that do not have a tag, and images that have been built locally (like `re-ranker:latest`, `comfyui:latest`).