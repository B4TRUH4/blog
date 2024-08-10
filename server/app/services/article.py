from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ..schemas import ArticleCreate, ArticleUpdate
from ..models import Article


async def get_article_by_id(
        db: AsyncSession,
        article_id: int) -> Article | None:
    """Получение статьи по id"""
    article = await db.get(Article, article_id)
    return article


async def get_article_with_comments_by_id(
        db: AsyncSession,
        article_id: int) -> Article | None:
    """Получение статьи по id с комментариями"""
    article = await db.get(
        Article,
        article_id,
        options=[joinedload(Article.comments)]
    )
    return article


async def list_articles(db: AsyncSession) -> Sequence[Article]:
    """Получение списка статей"""
    articles = await db.execute(
        select(Article).options(joinedload(Article.category))
    )
    return articles.scalars().all()


async def create_article(
        db: AsyncSession,
        article_data: ArticleCreate,
        user_id: int) -> Article:
    """Создание статьи"""
    article = Article(**article_data.dict(), author_id=user_id)
    db.add(article)
    await db.commit()
    await db.refresh(article)
    return article


async def delete_article(db: AsyncSession, article: Article):
    """Удаление статьи"""
    await db.delete(article)
    await db.commit()


async def update_article(
        db: AsyncSession,
        article: Article,
        updated_article: ArticleUpdate) -> Article:
    """Обновление статьи"""
    for key, value in updated_article.model_dump(exclude_unset=True).items():
        setattr(article, key, value)
    await db.commit()
    return article
