from app.services.matching import cosine

def test_cosine_identity():
    assert round(cosine([1,0,0], [1,0,0]), 5) == 1.0

def test_cosine_orthogonal():
    assert round(cosine([1,0], [0,1]), 5) == 0.0
