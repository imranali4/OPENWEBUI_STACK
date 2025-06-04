import torch
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# --- Define the Hugging Face Model Name ---
# This tells transformers where to find the model (it will look in HF_HOME cache first, then download)
MODEL_NAME = "BAAI/bge-reranker-v2-m3"

# --- Device Configuration ---
# Use MPS if available (for Apple Silicon), otherwise fall back to CPU
# Removed 'local_path' and 'local_files_only'
device = torch.device("mps") if torch.backends.mps.is_built() else torch.device("cpu")

# --- Load Model and Tokenizer from Hugging Face Hub ---
# transformers will automatically handle downloading and caching if the model isn't found locally
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Load the model directly by name.
# Ensure torch_dtype is compatible with the device. float16 is usually good for GPUs/MPS.
# If running on CPU exclusively, you might omit torch_dtype or use torch.float32.
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 # Keep this for MPS, it will be ignored on CPU if not applicable
).to(device)

# FastAPI app
app = FastAPI(title="BGE Reranker")

class Pair(BaseModel):
    query: str
    candidate: str

class RerankRequest(BaseModel):
    pairs: list[Pair]

class RerankResponse(BaseModel):
    scores: list[float]

@app.post("/rerank", response_model=RerankResponse)
def rerank(req: RerankRequest):
    texts = [p.query for p in req.pairs] + [p.candidate for p in req.pairs]
    enc = tokenizer(texts, padding=True, truncation=True, return_tensors="pt").to(device)
    with torch.no_grad():
        logits = model(**enc).logits.squeeze(-1)
    scores = logits.view(2, -1).t()[:, 1].cpu().tolist()
    return RerankResponse(scores=scores)