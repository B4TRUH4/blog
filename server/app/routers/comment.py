from .. import services
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import current_active_user
from app.auth.models import User
from ..schemas import CommentRead, CommentCreate
from ..dependencies import get_async_session

router = APIRouter(prefix='/comments', tags=['comments'])


@router.get('/', response_model=list[CommentRead], responses={
    status.HTTP_404_NOT_FOUND: {
        "description": "Article with id {id} does not exist"
    }
})
async def list_comments(
        article_id: int,
        db: AsyncSession = Depends(get_async_session)):
    article = await services.get_article_with_comments_by_id(db, article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with id {article_id} does not exist."
        )
    return article.comments


@router.post(
    '/',
    response_model=CommentRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Article with id {id} does not exist"
        },
        status.HTTP_403_FORBIDDEN: {"description": "Forbidden"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}
    }
)
async def create_comment(
        article_id: int,
        comment: CommentCreate,
        user: User = Depends(current_active_user),
        db: AsyncSession = Depends(get_async_session)):
    article = await services.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with id {article_id} does not exist."
        )
    comment = await services.create_comment(db, article_id, comment, user.id)
    return comment


@router.delete(
    '/{comment_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Comment does not exist"},
        status.HTTP_403_FORBIDDEN: {"description": "Forbidden"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}
    }
)
async def delete_comment(
        article_id: int,
        comment_id: int,
        user: User = Depends(current_active_user),
        db: AsyncSession = Depends(get_async_session)):
    comment = await services.get_comment_by_id(db, comment_id, article_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if comment.author_id != user.id and not user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await services.delete_comment(db, comment)


@router.put('/{comment_id}', response_model=CommentCreate, responses={
    status.HTTP_404_NOT_FOUND: {"description": "Comment does not exist"},
    status.HTTP_403_FORBIDDEN: {"description": "Forbidden"},
    status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}
})
async def update_comment(
        article_id: int,
        comment_id: int,
        updated_comment: CommentCreate,
        user: User = Depends(current_active_user),
        db: AsyncSession = Depends(get_async_session)):
    comment = await services.get_comment_by_id(db, article_id, comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if comment.author_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return await services.update_comment(db, comment, updated_comment)
