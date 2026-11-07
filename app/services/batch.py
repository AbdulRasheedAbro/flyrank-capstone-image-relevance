from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Image, Job
from app.services.ai import vision_analyze, embed
from app.services.repository import log_cost
from app.config import settings

def process_images(db: Session, job: Job):
    images = db.query(Image).filter(Image.status.in_(["pending", "failed"])).limit(settings.batch_size).all()
    job.total = len(images)
    db.commit()

    for image in images:
        success = False
        for attempt in range(settings.max_retries):
            image.processing_attempts += 1
            try:
                result = vision_analyze(image.path)
                image.subject = result.subject
                image.category = result.category
                image.attributes = result.attributes
                image.caption = result.caption
                image.confidence = result.confidence
                image.low_confidence = result.confidence < settings.vision_confidence_threshold
                image.embedding = embed(f"{result.subject}. {result.caption}. {' '.join(result.attributes)}")
                image.status = "processed"
                image.last_error = None
                log_cost(db, "ollama", "vision", settings.ollama_vision_model, str(image.id))
                log_cost(db, "ollama", "embedding", settings.ollama_embed_model, str(image.id))
                success = True
                job.processed += 1
                break
            except Exception as exc:
                image.last_error = str(exc)
                image.status = "failed"
                db.commit()
        if not success:
            job.failed += 1
        db.commit()

    job.status = "completed" if job.failed == 0 else "completed_with_errors"
    job.finished_at = datetime.utcnow()
    db.commit()
