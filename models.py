from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(String, unique=True, nullable=True)
    airline = Column(String, nullable=True)
    text = Column(Text, nullable=False)
    true_sentiment = Column(String, nullable=True)
    true_reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    analyses = relationship(
        "Analysis",
        back_populates="comment",
        cascade="all, delete-orphan",
    )


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(
        Integer,
        ForeignKey("comments.id"),
        nullable=False,
    )
    model = Column(String, nullable=True)
    prompt_version = Column(String, nullable=True)
    sentiment = Column(String, nullable=True)
    category = Column(String, nullable=True)
    urgency = Column(String, nullable=True)
    department = Column(String, nullable=True)
    tokens_used = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    comment = relationship(
        "Comment",
        back_populates="analyses",
    )