from __future__ import annotations

import os
import requests

# ---- Config via env vars (override as needed) ----
OLLAMA_HOST        = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL       = os.environ.get("OLLAMA_MODEL_NAME", "llama3.3:70b")
OLLAMA_TIMEOUT     = float(os.environ.get("OLLAMA_TIMEOUT", "2400"))   # seconds
OLLAMA_NUM_CTX     = int(os.environ.get("OLLAMA_NUM_CTX", "8192"))
OLLAMA_NUM_PREDICT = int(os.environ.get("OLLAMA_NUM_PREDICT", "-1"))  # -1 = unlimited
OLLAMA_TEMPERATURE = float(os.environ.get("OLLAMA_TEMPERATURE", "0.6"))
OLLAMA_TOP_P       = float(os.environ.get("OLLAMA_TOP_P", "0.9"))

DEFAULT_OPTIONS = {
    "temperature": float(os.environ.get("OLLAMA_TEMPERATURE", "0.85")),
    "top_p": float(os.environ.get("OLLAMA_TOP_P", "0.92")),
    "top_k": int(os.environ.get("OLLAMA_TOP_K", "50")),
    "num_ctx": int(os.environ.get("OLLAMA_NUM_CTX", "8192")),
    "num_predict": int(os.environ.get("OLLAMA_NUM_PREDICT", "-1")),
    "repeat_penalty": float(os.environ.get("OLLAMA_REPEAT_PENALTY", "1.18")),
    "repeat_last_n": int(os.environ.get("OLLAMA_REPEAT_LAST_N", "256")),
    # Optional: uncomment to try Mirostat
    # "mirostat": 2, "mirostat_tau": 5.0, "mirostat_eta": 0.1,
}

def llm(prompt: str, **options) -> str:
    url = f"{OLLAMA_HOST.rstrip('/')}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {**DEFAULT_OPTIONS, **options},
    }
    try:
        r = requests.post(url, json=payload, timeout=OLLAMA_TIMEOUT)
        r.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        raise RuntimeError(f"Cannot reach Ollama at {url}. Is it running?") from e
    except requests.exceptions.Timeout as e:
        raise RuntimeError(f"Ollama request timed out after {OLLAMA_TIMEOUT}s.") from e
    except requests.HTTPError as e:
        try:
            detail = r.json()
        except Exception:
            detail = r.text
        raise RuntimeError(f"Ollama error {r.status_code}: {detail}") from e
    return (r.json().get("response") or "").strip()