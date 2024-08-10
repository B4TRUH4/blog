from fastapi_filter.contrib.sqlalchemy import Filter
from .models import Article


class ArticleFilter(Filter):
    title__like: str | None = None
    content__like: str | None = None
    author_id: int | None = None
    category_id: int | None = None
    order_by: list[str] | None = None

    class Constants(Filter.Constants):
        model = Article
