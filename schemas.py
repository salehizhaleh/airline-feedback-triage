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

class AnalysisOut(BaseModel):
    id: int
    comment_id: int
    model: str
    prompt_version: str
    sentiment: str
    category: str
    urgency: str
    department: str
    tokens_used: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)