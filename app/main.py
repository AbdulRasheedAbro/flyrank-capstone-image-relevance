from fastapi import FastAPI
from app.api import router

app = FastAPI(title="FlyRank AI Image Matching Engine", version="1.0.0")
app.include_router(router)

@app.get("/")
def root():
    return {"name": "FlyRank AI Image Matching Engine", "status": "ready"}

@app.get("/health")
def health():
    return {"status": "ok"}
