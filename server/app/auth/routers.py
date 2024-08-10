from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .managers import UserManager
from .models import User
from .schemas import UserCreate, UserRead, UserUpdate
from .dependencies import (
    fastapi_users,
    auth_backend,
    get_user_manager,
    current_active_superuser
)
from ..dependencies import get_async_session

router = APIRouter()

users_router = fastapi_users.get_users_router(UserRead, UserUpdate)


@users_router.post("/{id}/make-superuser", response_model=UserRead)
async def make_superuser(
        user_id: int,
        user_manager: UserManager = Depends(get_user_manager),
        db: AsyncSession = Depends(get_async_session),
        _: User = Depends(current_active_superuser)):
    """Эндпоинт для предоставления прав администратора"""

    user = await user_manager.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user.is_superuser = True
    await db.commit()
    return user


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)


@users_router.post("/{id}/ban", response_model=UserRead)
async def make_superuser(
        user_id: int,
        user_manager: UserManager = Depends(get_user_manager),
        db: AsyncSession = Depends(get_async_session),
        _: User = Depends(current_active_superuser)):
    """Эндпоинт для бана пользователя"""

    user = await user_manager.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user.is_active = False
    await db.commit()
    return user


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)


@users_router.post("/{id}/unban", response_model=UserRead)
async def make_superuser(
        user_id: int,
        user_manager: UserManager = Depends(get_user_manager),
        db: AsyncSession = Depends(get_async_session),
        _: User = Depends(current_active_superuser)):
    """Эндпоинт для разбана пользователя"""

    user = await user_manager.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user.is_active = True
    await db.commit()
    return user


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)

router.include_router(
    fastapi_users.get_register_router(
        UserRead,
        UserCreate
    ),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    users_router,
    prefix="/users",
    tags=["users"],
)
