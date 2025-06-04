# OPENWEBUI_STACK - Comprehensive AI Stack

This repository contains a full AI stack orchestrated with Docker Compose, featuring:
*   **Open WebUI:** A user-friendly interface for your LLM interactions.
*   **BAAI/bge-reranker-v2-m3:** A powerful hybrid reranker for improved search relevance.
*   **SearXNG:** A privacy-respecting metasearch engine.
*   **Tika:** For content extraction.
*   **TTS Piper:** For text-to-speech capabilities.

This stack is designed to be easily deployed by users with Docker Desktop.

---

## Getting Started

Follow these steps to set up and run the full AI stack on your machine.

### Prerequisites

*   **Docker Desktop:** Ensure Docker Desktop is installed and running on your Windows, macOS, or Linux machine.
    *   Download from: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
*   **Git:** You'll need Git installed to clone this repository.
    *   Download from: [https://git-scm.com/downloads](https://git-scm.com/downloads)

### Project Structure

```
After cloning, your project directory (`OPENWEBUI_STACK`) will have the following structure:
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

### Step 3: Run the Full Stack

This command will build any necessary custom images, download external models (like the reranker model from Hugging Face), and start all the services defined in `docker-compose.yml`.

1.  Make sure you are in the `OPENWEBUI_STACK` directory in your terminal.
2.  Execute the following command:
    ```bash
    docker compose up --build -d
    ```
    *   `up`: Starts the services.
    *   `--build`: This is crucial! It tells Docker Compose to build your custom `hybridreranker` image before starting the containers. During this build, the `BAAI/bge-reranker-v2-m3` model will be downloaded and cached within the image.
    *   `-d`: Runs the containers in "detached" mode (in the background), so your terminal remains free. If you want to see all logs directly, remove `-d`.

    Allow some time for Docker to download images, build your custom image, and download the reranker model.

### Step 4: Access the Services

Once the services are up and running, you can access them via your web browser:

*   **Open WebUI:**
    *   Go to: `http://localhost:3000`
    *   **Note on LLM:** Open WebUI is configured to connect to an LLM running on `http://host.docker.internal:1234/v1`. This assumes you have a compatible LLM (like Ollama or a local LLM server) running on your Docker host machine, serving on port `1234`. If you don't, Open WebUI's AI features won't work immediately.
*   **SearXNG Search Engine (via Caddy proxy):**
    *   Go to: `http://localhost:8080`
*   **Tika (Content Extraction):** (Primarily for internal use by Open WebUI if configured for RAG)
    *   Accessible at: `http://localhost:9998`
*   **Hybrid Reranker:** (Primarily for internal use)
    *   Accessible at: `http://localhost:8999`
*   **TTS Piper (Text-to-Speech):** (Primarily for internal use)
    *   Accessible at: `http://localhost:8000`
    **ComfyUI Integration:** This stack automatically configures Open WebUI to connect to the included ComfyUI service for image generation.
        *   To use ComfyUI from Open WebUI, navigate to **Settings (gear icon) > Image Generation (Experimental)**.
        *   You will find `ComfyUI` pre-selected as the **Image Generation Engine**.
        *   **Important: You must upload a `workflow.json` file as API format** via the "ComfyUI Workflow" section in Open WebUI's settings. You can export an example workflow from ComfyUI itself (e.g., from `http://localhost:8188`) by selecting `Save (API Format)` from the `Save` menu.
        *   Once a workflow is uploaded, you can then configure the specific node IDs and parameters (Prompt, Model, Width, Height, etc.) directly in Open WebUI's settings.
*   **ComfyUI (Stable Diffusion UI):**
    *   Go to: `http://localhost:8188`
    *   You can directly access ComfyUI's web interface here to load workflows, generate images, and manage models. Remember to place your large Stable Diffusion models (checkpoints, Loras, VAEs, etc.) into the `OPENWEBUI_STACK/comfyui/models` directory on your host machine before starting the stack.

### Step 5: Stop the Services

When you're done, you can stop all running containers:

*   Navigate back to the `OPENWEBUI_STACK` directory in your terminal.
*   Run:
    ```bash
    docker compose down
    ```
    This will stop and remove the containers and networks. **Your data (e.g., Open WebUI database, SearXNG data) stored in Docker volumes will be preserved.**

### Step 6: Clean Up (Optional: Delete all data and images)

If you want to completely remove all data, containers, networks, and locally built images, use this command:

*   Navigate back to the `OPENWEBUI_STACK` directory in your terminal.
*   Run:
    ```bash
    docker compose down --volumes --rmi local
    ```
    *   `--volumes` (or `-v`): Removes the named Docker volumes, which store your persistent data. **This will delete your data.**
    *   `--rmi local`: Removes images that do not have a tag, and images that have been built locally (like `re-ranker:latest`).

---

---

**Now, here's what you need to do in your terminal:**

1.  Make sure you are in your `OPENWEBUI_STACK` directory.
2.  Open your `README.md` file using a text editor (e.g., `nano README.md` or open it with VS Code).
3.  **Paste all of the content provided above** into your `README.md` file.
4.  Save and close the `README.md` file.
5.  Stage your `README.md` file's changes:
    ```bash
    git add README.md
    ```
6.  Commit the changes:
    ```bash
    git commit -m "Add comprehensive README.md instructions"
    ```
7.  Push the changes to GitHub:
    ```bash
    git push -u origin main
    ```
    (You will be prompted for your username and PAT).

Once that's done, your `README.md` on GitHub will be fully populated with clear instructions for anyone wanting to use your stack!