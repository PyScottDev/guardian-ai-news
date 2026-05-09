from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager

from app.services.guardian import fetch_articles, fetch_body
from app.services.gemini import simplify_headline, simplify_body
from app.schemas import ArticlePreview, GeminiHeadlines, GeminiBody
from app.database.session import create_db_and_tables, SessionDep
from app.database.crud import article_check, db_full, create_headlines, update_body
from app.database.models import SimplifiedArticles

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
def home():
    return {"message": "Guardian AI News API is running"}


@app.get("/articles/{topic}/{level}", response_model=list[SimplifiedArticles])
async def get_articles(topic: str, level: str, session: SessionDep):
    existing_articles = article_check(session, topic, level)
    if existing_articles:
        return existing_articles
    articles = await fetch_articles(topic)
    simplified_headlines = await simplify_headline(articles, level)
    saved_articles = create_headlines(
        session=session,
        original_articles=articles,
        simplified_articles=simplified_headlines,
        topic=topic,
        level=level,
        )
    return saved_articles

@app.get("/article/{article_id}/{level}", response_model=SimplifiedArticles)
async def get_body(article_id: int, level: str, session: SessionDep):
    db_article = db_full(session, article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    if db_article.body:
        return db_article
    full_article = await fetch_body(db_article.guardian_id)
    simplified_body = await simplify_body(full_article, level)
    updated_article = update_body(session, db_article, simplified_body)
    return updated_article

    
    
    

    