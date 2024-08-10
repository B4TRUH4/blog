from typing import Sequence

from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ..schemas import ReviewCreate, ReviewUpdate
from ..models import Review


async def get_review_by_id(
        db: AsyncSession,
        review_id: int,
        article_id: int) -> Review:
    """Получение отзыва по id комментария и id статьи"""
    review = await db.scalar(
        select(Review).filter_by(
            article_id=article_id,
            id=review_id
        )
    )
    return review


async def get_review_with_author(
        db: AsyncSession,
        review_id: int,
        article_id: int) -> Review:
    """Получение отзыва с его автором"""
    review = await db.scalar(
        select(Review).filter_by(
            article_id=article_id,
            id=review_id
        ).options(joinedload(Review.author))
    )
    return review


async def list_reviews(
        db: AsyncSession,
        article_id: int) -> ScalarResult[Review]:
    """Получение списка отзывов"""
    reviews = await db.scalars(
        select(Review).filter_by(article_id=article_id)
    )
    return reviews


async def create_review(
        db: AsyncSession,
        article_id: int,
        review_data: ReviewCreate,
        user_id: int) -> Review:
    """Создание отзыва"""
    review = Review(
        **review_data.dict(),
        article_id=article_id,
        author_id=user_id
    )
    db.add(review)
    await db.commit()
    return review


async def delete_review(db: AsyncSession, review: Review):
    """Удаление отзыва"""
    await db.delete(review)
    await db.commit()


async def update_review(
        db: AsyncSession,
        review: Review,
        updated_review: ReviewUpdate) -> Review:
    """Обновление отзыва"""
    for key, value in updated_review.model_dump(exclude_unset=True).items():
        setattr(review, key, value)
    await db.commit()
    return review
