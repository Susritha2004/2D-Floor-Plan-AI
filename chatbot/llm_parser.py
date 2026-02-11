from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "google/flan-t5-base"

# Load once at startup (VERY IMPORTANT)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def parse_requirements(text):
    prompt = f"""
Extract house requirements from the text below.

Return JSON like:
{{
  "facing": "south",
  "rooms": [
    {{"name": "bedroom", "width": 11, "height": 11, "count": 2}},
    {{"name": "hall", "width": 12, "height": 15, "count": 1}}
  ]
}}

Text:
{text}

JSON:
"""

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(**inputs, max_new_tokens=200)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return result
