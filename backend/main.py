import sys
sys.path.insert(0, "D:\\contentforge-ai")

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.db import get_db, init_db, GeneratedContent
from main_crew import run_content_crew
import json

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="ContentForge AI", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContentRequest(BaseModel):
    subject: str

@app.get("/")
async def root():
    return {"message": "ContentForge AI is running", "version": "1.0.0"}

@app.post("/generate")
async def generate_content(request: ContentRequest, db: Session = Depends(get_db)):
    try:
        result = run_content_crew(request.subject)

        # Handle both dict and pydantic object safely
        if isinstance(result, dict):
            article = result.get("article", "")
            subject = result.get("subject", request.subject)
            word_count = result.get("word_count", len(article.split()))
            social_posts_raw = result.get("social_media_posts", [])
            social_media_posts = social_posts_raw
        else:
            article = getattr(result, "article", "")
            subject = getattr(result, "subject", request.subject)
            word_count = getattr(result, "word_count", len(article.split()))
            social_posts_raw = getattr(result, "social_media_posts", [])
            social_media_posts = [
                p.dict() if hasattr(p, "dict") else p
                for p in social_posts_raw
            ]

        # Save to database
        record = GeneratedContent(
            subject=subject,
            article=article,
            social_posts=json.dumps(social_media_posts),
            word_count=word_count,
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        return {
            "id": record.id,
            "subject": subject,
            "article": article,
            "social_media_posts": social_media_posts,
            "word_count": word_count,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_history(db: Session = Depends(get_db)):
    records = db.query(GeneratedContent).order_by(
        GeneratedContent.created_at.desc()
    ).limit(20).all()
    return records