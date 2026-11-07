import base64, json, re
from pathlib import Path
import requests
from app.config import settings
from app.schemas import VisionResult

def _extract_json(text: str) -> dict:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.S)
        if not match:
            raise ValueError("Vision model did not return JSON")
        return json.loads(match.group(0))

def vision_analyze(path: str) -> VisionResult:
    if settings.mock_ai:
        name = Path(path).stem.lower()
        if "fox" in name:
            return VisionResult(subject="red fox", category="animal",
                attributes=["orange fur","wild","forest"],
                caption="A red fox standing in a forest", confidence=0.96)
        if "wolf" in name:
            return VisionResult(subject="gray wolf", category="animal",
                attributes=["gray fur","wild","forest"],
                caption="A gray wolf in a forest", confidence=0.96)
        return VisionResult(subject=name, category="animal",
            attributes=["wild"], caption=f"An image of {name}", confidence=0.80)

    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    encoded = base64.b64encode(p.read_bytes()).decode()
    prompt = (
        "Analyze this image. Return ONLY valid JSON with exactly these keys: "
        "subject, category, attributes, caption, confidence. "
        "confidence must be a number from 0 to 1. Be specific about the main subject."
    )
    r = requests.post(
        f"{settings.ollama_base_url}/api/generate",
        json={"model": settings.ollama_vision_model, "prompt": prompt,
              "images": [encoded], "stream": False, "format": "json"},
        timeout=180
    )
    r.raise_for_status()
    result = VisionResult.model_validate(_extract_json(r.json()["response"]))
    return result

def embed(text: str) -> list[float]:
    if settings.mock_ai:
        # Deterministic small vectors for tests/demo; production uses Ollama.
        import hashlib, math
        digest = hashlib.sha256(text.lower().encode()).digest()
        return [((digest[i] / 255.0) * 2 - 1) for i in range(16)]

    payload = {"model": settings.ollama_embed_model, "input": text}
    r = requests.post(f"{settings.ollama_base_url}/api/embed", json=payload, timeout=120)
    if r.status_code >= 400:
        r = requests.post(f"{settings.ollama_base_url}/api/embeddings",
                           json={"model": settings.ollama_embed_model, "prompt": text},
                           timeout=120)
    r.raise_for_status()
    data = r.json()
    if "embeddings" in data:
        return data["embeddings"][0]
    return data["embedding"]
