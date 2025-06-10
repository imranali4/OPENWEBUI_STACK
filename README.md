# OPENWEBUI_STACK - Comprehensive AI & Automation Stack

This repository contains a full AI and automation stack orchestrated with Docker Compose, featuring:
*   **Open WebUI:** A user-friendly interface for your LLM interactions.
*   **BAAI/bge-reranker-v2-m3:** A powerful hybrid reranker for improved search relevance.
*   **SearXNG:** A privacy-respecting metasearch engine.
*   **Tika:** For content extraction.
*   **TTS Piper:** For text-to-speech capabilities.
*   **n8n:** A powerful workflow automation tool to connect APIs and automate tasks.

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

OPENWEBUI_STACK/ 
├── docker-compose.yml # The main Docker Compose orchestration file 
├── hybridreranker/ # Contains Dockerfile and code for the custom reranker 
│ 
├── Dockerfile 
│ 
├── inference.py 
│ 
└── requirements.txt 
├── my_custom_tools/ # Custom tool scripts for Open WebUI 
│ 
└── example_tool.py 
├── openedai-speech/ # Configuration and voice models for TTS Piper 
│ 
├── config/ 
│ 
│ 
└── ... 
│ 
└── voices/ 
│ 
└── ... 
├── searxng-docker/ # Configuration for SearXNG 
│ 
└── searxng/ 
│ 
└── settings.yml 
│ 
└── ... 
├── .env.example # Template for environment variables (e.g., API keys) 
├── .gitignore # Specifies files/folders Git should ignore 
└── README.md # This guide!