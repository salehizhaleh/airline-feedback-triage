from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CommentCreate(BaseModel):
    tweet_id: Optional[str] = None
    airline: Optional[str] = None
    text: str
    true_sentiment: Optional[str] = None
    true_reason: Optional[str] = None


class CommentOut(CommentCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)