from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas import CommentCreate
from ..models import Comment


async def get_comment_by_id(
        db: AsyncSession,
        comment_id: int,
        article_id: int) -> Comment:
    """Получение комментария по id комментария и id статьи"""
    comment = await db.scalar(
        select(Comment).filter_by(article_id=article_id, id=comment_id)
    )
    return comment


async def list_comments(db: AsyncSession, article_id: int) -> Sequence[Comment]:
    """Получение списка комментариев"""
    comments = await db.scalars(
        select(Comment).filter_by(article_id=article_id)
    )
    return comments


async def create_comment(
        db: AsyncSession,
        article_id: int,
        comment_data: CommentCreate,
        user_id: int) -> Comment:
    """Создание комментария"""
    comment = Comment(
        **comment_data.dict(),
        article_id=article_id,
        author_id=user_id
    )
    db.add(comment)
    await db.commit()
    return comment


async def delete_comment(db: AsyncSession, comment: Comment):
    """Удаление комментария"""
    await db.delete(comment)
    await db.commit()


async def update_comment(
        db: AsyncSession,
        comment: Comment,
        updated_comment: CommentCreate) -> Comment:
    """Обновление комментария"""
    for key, value in updated_comment.model_dump(exclude_unset=True).items():
        setattr(comment, key, value)
    await db.commit()
    return comment
