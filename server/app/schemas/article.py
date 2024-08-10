from pydantic import BaseModel, field_validator
from .category import CategoryRead


class ArticleBase(BaseModel):
    title: str
    category_id: int


class ArticleBaseRead(ArticleBase):
    id: int
    author_id: int
    category: CategoryRead


class ArticleDetailRead(ArticleBaseRead):
    content: str


class ArticleCreate(ArticleBase):
    content: str


class ArticleUpdate(ArticleBase):
    content: str | None = None
    title: str | None = None
    category_id: int | None = None
