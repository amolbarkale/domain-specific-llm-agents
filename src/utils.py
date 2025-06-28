import os
import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Load once globally to save time
MODEL_NAME = "google/flan-t5-small"
MODEL_CACHE_DIR = "/c/Users/Amol Barkale/.cache/huggingface/hub/models--google--flan-t5-small"

# Load model + tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_CACHE_DIR)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_CACHE_DIR)

# Ensure model is on the right device
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(DEVICE)


def load_prompt_template(filepath: str) -> str:
    """Load a raw prompt template from a text file"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt file not found: {filepath}")
    
    with open(filepath, 'r') as f:
        return f.read().strip()


def save_json(data, path: str):
    """Save JSON to file with indentation"""
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def call_llm(prompt: str, max_tokens: int = 256, temperature: float = 0.7) -> str:
    """
    Call FLAN-T5-Small model locally using Transformers.
    Returns generated response as plain string.
    """
    # Tokenize input
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to(DEVICE)

    # Generate
    outputs = model.generate(
        inputs["input_ids"],
        max_length=max_tokens,
        temperature=temperature,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id
    )

    # Decode and return
    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
