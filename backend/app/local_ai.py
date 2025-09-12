from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Example: MPT-7B-Instruct quantized or small instruct model
MODEL_NAME = "mosaicml/mpt-7b-instruct"  # free, Hugging Face

# Load tokenizer & model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="auto", torch_dtype=torch.float16)

def personalize_email(lead: dict, template: str) -> dict:
    """
    Generate subject and body using local open-source model
    """
    prompt = f"""
You are a sales assistant. Personalize the following template for this lead:
Lead: {lead}
Template: {template}

Return a JSON with keys: subject, body
"""
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=150)
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Try simple JSON parsing (naive)
    import json
    try:
        # Extract JSON from model text
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])
    except Exception:
        return {"subject": f"Quick question for {lead.get('name','there')}", "body": template}

def classify_reply(text: str) -> dict:
    """
    Simple classification: interested / not_interested / follow_up_later
    """
    prompt = f"""
Classify the reply into one of these: interested, not_interested, follow_up_later
Reply: {text}
Return JSON: {{ "label": ..., "reason": ... }}
"""
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=50)
    resp = tokenizer.decode(outputs[0], skip_special_tokens=True)
    import json
    try:
        start = resp.find("{")
        end = resp.rfind("}") + 1
        return json.loads(resp[start:end])
    except Exception:
        return {"label": "follow_up_later", "reason": resp}
