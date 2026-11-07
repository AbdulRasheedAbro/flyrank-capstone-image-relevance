from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Image, Post, Job, Suggestion
from app.schemas import ImageCreate, PostCreate, ImageOut, PostOut, JobOut, SuggestionOut
from app.services.batch import process_images
from app.services.matching import create_suggestions

router = APIRouter()

@router.post("/images", response_model=ImageOut)
def create_image(payload: ImageCreate, db: Session = Depends(get_db)):
    existing = db.query(Image).filter(Image.path == payload.path).first()
    if existing:
        return existing
    image = Image(path=payload.path)
    db.add(image); db.commit(); db.refresh(image)
    return image

@router.post("/posts", response_model=PostOut)
def create_post(payload: PostCreate, db: Session = Depends(get_db)):
    post = Post(title=payload.title, body=payload.body)
    db.add(post); db.commit(); db.refresh(post)
    return post

@router.post("/jobs/process-images", response_model=JobOut)
def start_processing(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    active = db.query(Job).filter(Job.job_type == "image_processing", Job.status.in_(["queued", "running"])).first()
    if active:
        return active
    job = Job(job_type="image_processing", status="running")
    db.add(job); db.commit(); db.refresh(job)
    background_tasks.add_task(_run_batch, job.id)
    return job

def _run_batch(job_id: int):
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        job = db.get(Job, job_id)
        if job:
            process_images(db, job)
    finally:
        db.close()

@router.get("/jobs/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if not job: raise HTTPException(404, "Job not found")
    return job

@router.get("/posts/{post_id}/images", response_model=list[SuggestionOut])
def match_post(post_id: int, db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if not post: raise HTTPException(404, "Post not found")
    return create_suggestions(db, post)

@router.get("/suggestions/{suggestion_id}/why", response_model=SuggestionOut)
def why(suggestion_id: int, db: Session = Depends(get_db)):
    item = db.get(Suggestion, suggestion_id)
    if not item: raise HTTPException(404, "Suggestion not found")
    return item

@router.post("/suggestions/{suggestion_id}/approve", response_model=SuggestionOut)
def approve(suggestion_id: int, db: Session = Depends(get_db)):
    item = db.get(Suggestion, suggestion_id)
    if not item: raise HTTPException(404, "Suggestion not found")
    item.decision = "APPROVED"; db.commit(); db.refresh(item); return item

@router.post("/suggestions/{suggestion_id}/reject", response_model=SuggestionOut)
def reject(suggestion_id: int, db: Session = Depends(get_db)):
    item = db.get(Suggestion, suggestion_id)
    if not item: raise HTTPException(404, "Suggestion not found")
    item.decision = "REJECTED_BY_REVIEW"; db.commit(); db.refresh(item); return item
