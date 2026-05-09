from sqlmodel import SQLModel, Field

class ArticleBase(SQLModel):
    guardian_id:str
    headline: str
    subheadline: str | None = None
    
class ArticlePreview(ArticleBase):
    topic: str
    thumbnail: str | None = None
    
class ArticleFull(ArticleBase):
    topic: str
    thumbnail: str | None = None
    body: str | None = None

class GeminiHeadlines(ArticleBase):
    pass

class GeminiBody(ArticleBase):
    body: str
    questions: list[str] = Field(default_factory=list)
    
