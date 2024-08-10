from pydantic import BaseModel

from .article import ArticleDetailRead
from ..auth.schemas import UserRead


class ReportBase(BaseModel):
    content: str
    article_id: int


class ReportBaseRead(ReportBase):
    id: int
    author_id: int
    solved: bool


class ReportDetailRead(ReportBaseRead):
    author: UserRead
    article: ArticleDetailRead


class ReportCreate(ReportBase):
    pass
