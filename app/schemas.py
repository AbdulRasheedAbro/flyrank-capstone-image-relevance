from pydantic import BaseModel, Field, ConfigDict

class VisionResult(BaseModel):
    subject: str = Field(min_length=1)
    category: str = Field(min_length=1)
    attributes: list[str] = Field(default_factory=list)
    caption: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)

class ImageCreate(BaseModel):
    path: str

class PostCreate(BaseModel):
    title: str
    body: str

class ImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    path: str
    subject: str | None
    category: str | None
    attributes: list | None
    caption: str | None
    confidence: float | None
    status: str
    low_confidence: bool
    processing_attempts: int

class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    body: str

class JobOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    job_type: str
    status: str
    total: int
    processed: int
    failed: int
    error: str | None

class SuggestionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    post_id: int
    image_id: int | None
    similarity: float
    decision: str
    reason: str
