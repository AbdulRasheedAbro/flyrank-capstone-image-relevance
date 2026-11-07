from types import SimpleNamespace
from app.services.guard import guard

def image(subject="gray wolf", confidence=0.95):
    return SimpleNamespace(subject=subject, confidence=confidence)

def test_fox_post_rejects_wolf():
    decision, reason = guard("A red fox in a forest", image("gray wolf"), 0.90)
    assert decision == "REJECTED"
    assert "mismatch" in reason.lower()

def test_low_similarity_rejects():
    decision, reason = guard("fox", image("red fox"), 0.20)
    assert decision == "REJECTED"
    assert "similarity" in reason.lower()

def test_low_confidence_rejects():
    decision, reason = guard("fox", image("red fox", 0.40), 0.90)
    assert decision == "REJECTED"
    assert "confidence" in reason.lower()
