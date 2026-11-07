from app.config import settings
from app.models import Image

def guard(post_text: str, image: Image, similarity: float) -> tuple[str, str]:
    if similarity < settings.similarity_threshold:
        return "REJECTED", f"Semantic similarity below threshold ({similarity:.3f} < {settings.similarity_threshold:.3f})"
    if image.confidence is None or image.confidence < settings.vision_confidence_threshold:
        return "REJECTED", f"Vision confidence too low ({image.confidence or 0:.3f} < {settings.vision_confidence_threshold:.3f})"

    p = post_text.lower()
    subject = (image.subject or "").lower()
    if "fox" in p and "wolf" in subject:
        return "REJECTED", "Animal category mismatch: expected fox, detected wolf"
    if "wolf" in p and "fox" in subject:
        return "REJECTED", "Animal category mismatch: expected wolf, detected fox"
    return "ACCEPTED", "Passed semantic similarity, confidence, and mismatch checks"

def no_confident_match_reason(candidates: list[tuple[Image, float]]) -> str:
    if not candidates:
        return "No processed images are available."
    top = candidates[0][1]
    return f"No confident match. Best similarity was {top:.3f}, below threshold {settings.similarity_threshold:.3f}."
