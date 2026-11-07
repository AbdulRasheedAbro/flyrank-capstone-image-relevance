from sqlalchemy.orm import Session
from app.models import Image, Post, CostLog

def log_cost(db: Session, provider: str, operation: str, model: str, item_id: str, cost: float = 0.0):
    db.add(CostLog(provider=provider, operation=operation, model=model, item_id=item_id, cost_usd=cost))
