import re
import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


MODEL_NAME = "google/flan-t5-base"

# Load model once (very important)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


def build_prompt(text):
    return f"""
You are a strict JSON extraction engine.

Extract structured house requirements.

IMPORTANT RULES:
- Output ONLY valid JSON.
- No explanation.
- No text before or after JSON.
- All keys must match exactly.
- All string values must be lowercase.
- All numbers must be integers.
- If width or height not specified, use null.
- If count not specified, use 1.

Allowed room names:
- bedroom
- hall
- kitchen
- bathroom

Allowed facing values:
- north
- south
- east
- west
- null

Required JSON format:

{{
  "facing": "north|south|east|west|null",
  "rooms": [
    {{
      "name": "bedroom|hall|kitchen|bathroom",
      "width": int|null,
      "height": int|null,
      "count": int
    }}
  ]
}}

Text:
{text}

JSON:
"""


def extract_json_block(output):
    match = re.search(r"\{.*\}", output, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in model output")
    return match.group()


def parse_requirements_with_llm(text):
    prompt = build_prompt(text)

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)

    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.0,   # deterministic
        do_sample=False    # no randomness
    )

    raw_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

    json_block = extract_json_block(raw_output)

    try:
        parsed = json.loads(json_block)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON returned by model")

    return parsed
