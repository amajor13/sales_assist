# backend/local_ai.py
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import json

# Small, CPU-friendly model
MODEL_NAME = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

def personalize_email(lead: dict, template: str) -> dict:
    prompt = f"Personalize this template for the lead {lead}: {template}"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=50)
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"subject": f"Hello {lead.get('name','there')}", "body": text}

def classify_reply(text: str) -> dict:
    """Simple rule-based intent classifier for demo purposes"""

    t = text.lower()

    if any(word in t for word in ["yes", "interested", "let's talk", "okay", "sure"]):
        return {"label": "interested", "reason": text}

    if any(word in t for word in ["no", "not interested", "stop", "dont", "don't", "never"]):
        return {"label": "not_interested", "reason": text}

    if any(word in t for word in ["call later", "maybe", "busy", "follow up", "ping me"]):
        return {"label": "follow_up_later", "reason": text}

    # Default fallback
    return {"label": "unknown", "reason": text}
