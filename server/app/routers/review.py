from .. import services
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.dependencies import current_active_user
from ..auth.models import User
from ..schemas import ReviewRead, ReviewCreate, ReviewUpdate
from ..dependencies import get_async_session

router = APIRouter(prefix='/reviews', tags=['reviews'])


@router.get('/', response_model=list[ReviewRead], responses={
    status.HTTP_404_NOT_FOUND: {
        "description": "Article with id {id} does not exist"
    }
})
async def list_reviews(
        article_id: int,
        db: AsyncSession = Depends(get_async_session)):
    """Эндпоинт для просмотра списка отзывов"""
    article = await services.get_article_with_reviews_by_id(db, article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with id {article_id} does not exist."
        )
    return article.reviews


@router.post(
    '/',
    response_model=ReviewRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Article with id {id} does not exist"
        },
        status.HTTP_403_FORBIDDEN: {"description": "Forbidden"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}
    }
)
async def create_review(
        article_id: int,
        review: ReviewCreate,
        user: User = Depends(current_active_user),
        db: AsyncSession = Depends(get_async_session)):
    """Эндпоинт для создания отзыва"""
    article = await services.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with id {article_id} does not exist."
        )
    review = await services.create_review(db, article_id, review, user.id)
    return review


@router.get(
    '/{review_id}',
    response_model=ReviewRead,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Review does not exist"},
        status.HTTP_403_FORBIDDEN: {"description": "Forbidden"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}
    }
)
async def get_review(
        article_id: int,
        review_id: int,
        db: AsyncSession = Depends(get_async_session)):
    """Эндпоинт для просмотра отзыва"""
    review = await services.get_review_with_author(db, review_id, article_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review does not exist"
        )
    return review


@router.delete(
    '/{review_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Review does not exist"},
        status.HTTP_403_FORBIDDEN: {"description": "Forbidden"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}
    }
)
async def delete_review(
        article_id: int,
        review_id: int,
        user: User = Depends(current_active_user),
        db: AsyncSession = Depends(get_async_session)):
    """Эндпоинт для удаления отзыва"""
    review = await services.get_review_by_id(db, review_id, article_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review does not exist"
        )
    if review.author_id != user.id and not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    await services.delete_review(db, review)


@router.put('/{review_id}', response_model=ReviewRead, responses={
    status.HTTP_404_NOT_FOUND: {"description": "Review does not exist"},
    status.HTTP_403_FORBIDDEN: {"description": "Forbidden"},
    status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}
})
async def update_review(
        article_id: int,
        review_id: int,
        updated_review: ReviewUpdate,
        user: User = Depends(current_active_user),
        db: AsyncSession = Depends(get_async_session)):
    """Эндпоинт для изменения отзыва"""
    review = await services.get_review_with_author(db, article_id, review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review does not exist"
        )
    if review.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    return await services.update_review(db, review, updated_review)
