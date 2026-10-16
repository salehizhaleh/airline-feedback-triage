from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db
import analyzer


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/comments", response_model=schemas.CommentOut)
def create_comment(
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
):
    db_comment = models.Comment(**comment.model_dump())

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    return db_comment


@app.get("/comments", response_model=list[schemas.CommentOut])
def list_comments(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return (
        db.query(models.Comment)
        .offset(skip)
        .limit(limit)
        .all()
    )


@app.get("/comments/{comment_id}", response_model=schemas.CommentOut)
def get_comment(
    comment_id: int,
    db: Session = Depends(get_db),
):
    comment = db.get(models.Comment, comment_id)

    if comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found",
        )

    return comment


@app.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
):
    comment = db.get(models.Comment, comment_id)

    if comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found",
        )

    db.delete(comment)
    db.commit()

    return {"deleted": comment_id}


@app.post(
    "/comments/{comment_id}/analyze",
    response_model=schemas.AnalysisOut,
)
def analyze_comment(
    comment_id: int,
    db: Session = Depends(get_db),
):
    comment = db.get(models.Comment, comment_id)

    if comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found",
        )

    result = analyzer.analyze_text(comment.text)

    analysis = models.Analysis(
        comment_id=comment.id,
        model=analyzer.MODEL,
        prompt_version=analyzer.PROMPT_VERSION,
        **result,
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis


@app.get(
    "/analyses",
    response_model=list[schemas.AnalysisOut],
)
def list_analyses(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return (
        db.query(models.Analysis)
        .offset(skip)
        .limit(limit)
        .all()
    )