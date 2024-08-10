from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .. import services
from ..dependencies import get_async_session
from ..schemas import CategoryBase, CategoryRead
from ..auth.models import User
from ..auth.dependencies import current_active_superuser

router = APIRouter(prefix='/categories', tags=['categories'])


@router.get('/', response_model=list[CategoryRead])
async def list_categories(db: AsyncSession = Depends(get_async_session)):
    """Эндпоинт для просмотра списка категорий"""
    result = await services.list_categories(db)
    return result


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryRead,
    responses={
        status.HTTP_403_FORBIDDEN: {'description': 'Forbidden'}
    }
)
async def create_category(
        category: CategoryBase,
        _: User = Depends(current_active_superuser),
        db: AsyncSession = Depends(get_async_session)):
    """Эндпоинт для создания категории"""
    result = await services.create_category(db, category)
    return result


@router.delete(
    '/{category_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Category not found"},
        status.HTTP_403_FORBIDDEN: {"description": "Forbidden"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}
    }
)
async def delete_category(
        category_id: int,
        _: User = Depends(current_active_superuser),
        db: AsyncSession = Depends(get_async_session)):
    """Эндпоинт для просмотра категории"""
    category = await services.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    await services.delete_category(db, category)
