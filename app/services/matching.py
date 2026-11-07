import math
from sqlalchemy.orm import Session
from app.models import Image, Post, Suggestion
from app.services.ai import embed
from app.services.guard import guard, no_confident_match_reason

def cosine(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x*y for x,y in zip(a,b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(y*y for y in b))
    return dot/(na*nb) if na and nb else 0.0

def rank_images(db: Session, post: Post, limit: int = 10):
    if not post.embedding:
        post.embedding = embed(f"{post.title}. {post.body}")
        db.commit()
    candidates = []
    for image in db.query(Image).filter(Image.status == "processed").all():
        sim = cosine(post.embedding, image.embedding or [])
        candidates.append((image, sim))
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[:limit]

def create_suggestions(db: Session, post: Post, limit: int = 10):
    candidates = rank_images(db, post, limit)
    created = []
    accepted = False
    for image, sim in candidates:
        decision, reason = guard(post.body + " " + post.title, image, sim)
        s = Suggestion(post_id=post.id, image_id=image.id, similarity=sim,
                       decision=decision, reason=reason)
        db.add(s)
        created.append(s)
        if decision == "ACCEPTED" and not accepted:
            accepted = True
    if not accepted:
        s = Suggestion(post_id=post.id, image_id=None, similarity=candidates[0][1] if candidates else 0.0,
                       decision="NO_CONFIDENT_MATCH", reason=no_confident_match_reason(candidates))
        db.add(s)
        created.append(s)
    db.commit()
    return created
