from app.schemas import VisionResult

def test_vision_schema():
    item = VisionResult(subject="red fox", category="animal",
                        attributes=["orange fur"], caption="A red fox", confidence=0.94)
    assert item.confidence == 0.94
