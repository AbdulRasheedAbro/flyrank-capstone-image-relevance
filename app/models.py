from datetime import datetime
from sqlalchemy import String, Text, Float, Integer, Boolean, DateTime, ForeignKey, Index, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Image(Base):
    __tablename__ = "images"
    __table_args__ = (
        Index("ix_images_status", "status"),
        Index("ix_images_category", "category"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(String(500), unique=True)
    subject: Mapped[str | None] = mapped_column(String(200))
    category: Mapped[str | None] = mapped_column(String(100))
    attributes: Mapped[list | None] = mapped_column(JSON)
    caption: Mapped[str | None] = mapped_column(Text)
    confidence: Mapped[float | None] = mapped_column(Float)
    embedding: Mapped[list | None] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String(40), default="pending", index=True)
    processing_attempts: Mapped[int] = mapped_column(Integer, default=0)
    low_confidence: Mapped[bool] = mapped_column(Boolean, default=False)
    last_error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(300))
    body: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    job_type: Mapped[str] = mapped_column(String(60), index=True)
    status: Mapped[str] = mapped_column(String(40), default="queued", index=True)
    total: Mapped[int] = mapped_column(Integer, default=0)
    processed: Mapped[int] = mapped_column(Integer, default=0)
    failed: Mapped[int] = mapped_column(Integer, default=0)
    error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime)

class Suggestion(Base):
    __tablename__ = "suggestions"
    __table_args__ = (Index("ix_suggestions_post", "post_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    image_id: Mapped[int | None] = mapped_column(ForeignKey("images.id"))
    similarity: Mapped[float] = mapped_column(Float)
    decision: Mapped[str] = mapped_column(String(30))
    reason: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class CostLog(Base):
    __tablename__ = "cost_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    provider: Mapped[str] = mapped_column(String(80))
    operation: Mapped[str] = mapped_column(String(80))
    model: Mapped[str] = mapped_column(String(120))
    item_id: Mapped[str | None] = mapped_column(String(120))
    cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
