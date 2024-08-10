from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas import CategoryBase
from ..models import Category


async def list_categories(db: AsyncSession) -> Sequence[Category]:
    """Получение списка категорий"""
    categories = await db.scalars(select(Category))
    return categories.all()


async def get_category_by_id(
        db: AsyncSession,
        category_id: int) -> Category | None:
    """Получение категории по id"""
    category = await db.get(Category, category_id)
    return category


async def create_category(
        db: AsyncSession,
        category: CategoryBase) -> Category | None:
    """Создание категории"""
    db_category = Category(**category.dict())
    db.add(db_category)
    await db.commit()
    return db_category


async def delete_category(db: AsyncSession, category: Category):
    """Удаление категории"""
    await db.delete(category)
    await db.commit()
