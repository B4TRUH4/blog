from .. import services
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import current_active_user
from app.auth.models import User
from ..schemas import (
    ArticleBaseRead, ArticleDetailRead, ArticleCreate,
    ArticleUpdate
)
from ..dependencies import get_async_session
from .comment import router as comment_router
from .review import router as review_router

router = APIRouter(prefix='/articles', tags=['articles'])

router.include_router(comment_router, prefix='/{article_id}', tags=['comments'])
router.include_router(review_router, prefix='/{article_id}', tags=['reviews'])


@router.get('/', response_model=list[ArticleBaseRead])
async def list_articles(db: AsyncSession = Depends(get_async_session)):
    """Эндпоинт для просмотра списка статей"""
    article = await services.list_articles(db)
    return article


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=ArticleBaseRead,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Category with id {id} does not exist"
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}
    }
)
async def create_article(
        article: ArticleCreate,
        user: User = Depends(current_active_user),
        db: AsyncSession = Depends(get_async_session)):
    """Эндпоинт для создания статьи"""
    category = await services.get_category_by_id(db, article.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {article.category_id} does not exist."
        )
    article = await services.create_article(db, article, user.id)
    return article


@router.get('/{article_id}', response_model=ArticleDetailRead, responses={
    status.HTTP_404_NOT_FOUND: {"description": "Article not found"},
})
async def get_article(
        article_id: int,
        db: AsyncSession = Depends(get_async_session)):
    """Эндпоинт для просмотра статьи"""
    article = await services.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article not found"
        )
    return article


@router.delete(
    '/{article_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Article not found"},
        status.HTTP_403_FORBIDDEN: {"description": "Forbidden"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}
    }
)
async def delete_article(
        article_id: int,
        user: User = Depends(current_active_user),
        db: AsyncSession = Depends(get_async_session)):
    """Эндпоинт для удаления статьи"""
    article = await services.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    if article.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    await services.delete_article(db, article)


@router.put('/{article_id}', response_model=ArticleDetailRead, responses={
    status.HTTP_404_NOT_FOUND: {"description": "Article not found"},
    status.HTTP_403_FORBIDDEN: {"description": "Forbidden"},
    status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}
})
async def update_article(
        article_id: int,
        updated_article: ArticleUpdate,
        user: User = Depends(current_active_user),
        db: AsyncSession = Depends(get_async_session)):
    """Эндпоинт для обновления статьи"""
    article = await services.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    if article.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    return await services.update_article(db, article, updated_article)
