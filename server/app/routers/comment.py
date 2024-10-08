from .. import services
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.dependencies import current_active_user
from ..auth.models import User
from ..schemas import CommentRead, CommentCreate, CommentUpdate
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
    """Эндпоинт для просмотра списка комментариев"""
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
    """Эндпоинт для создания комментария"""
    article = await services.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with id {article_id} does not exist."
        )
    comment = await services.create_comment(db, article_id, comment, user.id)
    return comment


@router.get(
    '/{comment_id}',
    response_model=CommentRead,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Comment does not exist"},
        status.HTTP_403_FORBIDDEN: {"description": "Forbidden"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}
    }
)
async def get_comment(
        article_id: int,
        comment_id: int,
        db: AsyncSession = Depends(get_async_session)):
    """Эндпоинт для просмотра комментария"""
    comment = await services.get_comment_with_author(db, comment_id, article_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment does not exist"
        )
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
    """Эндпоинт для удаления комментария"""
    comment = await services.get_comment_by_id(db, comment_id, article_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment does not exist"
        )
    if comment.author_id != user.id and not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    await services.delete_comment(db, comment)


@router.put('/{comment_id}', response_model=CommentRead, responses={
    status.HTTP_404_NOT_FOUND: {"description": "Comment does not exist"},
    status.HTTP_403_FORBIDDEN: {"description": "Forbidden"},
    status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}
})
async def update_comment(
        article_id: int,
        comment_id: int,
        updated_comment: CommentUpdate,
        user: User = Depends(current_active_user),
        db: AsyncSession = Depends(get_async_session)):
    """Эндпоинт для изменения комментария"""
    comment = await services.get_comment_with_author(db, article_id, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment does not exist"
        )
    if comment.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    return await services.update_comment(db, comment, updated_comment)
