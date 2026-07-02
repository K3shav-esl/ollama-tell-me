import httpx
import os
import json

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:14b")

# Connect must succeed quickly; read can take as long as the model needs
TIMEOUT = httpx.Timeout(connect=10.0, read=None, write=30.0, pool=10.0)

def generate(prompt: str, system: str = "") -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "system": system,
        "stream": False
    }
    response = httpx.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=TIMEOUT)
    return response.json()["response"]

def generate_stream(prompt: str, system: str = ""):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "system": system,
        "stream": True
    }
    with httpx.stream("POST", f"{OLLAMA_URL}/api/generate", json=payload, timeout=TIMEOUT) as r:
        for line in r.iter_lines():
            if line:
                chunk = json.loads(line)
                if not chunk.get("done"):
                    yield chunk.get("response", "")