from .. import services
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.dependencies import current_active_user, current_active_superuser
from ..auth.models import User
from ..schemas import ReportBaseRead, ReportDetailRead, ReportCreate
from ..dependencies import get_async_session

router = APIRouter(prefix='/reports', tags=['reports'])


@router.get('/', response_model=list[ReportBaseRead])
async def list_reports(
        db: AsyncSession = Depends(get_async_session),
        _: User = Depends(current_active_superuser)):
    """Эндпоинт получения списка жалоб"""
    result = await services.list_reports(db)
    return result


@router.post(
    '/',
    response_model=ReportBaseRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Article with id {id} does not exist"
        },
        status.HTTP_403_FORBIDDEN: {"description": "Forbidden"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}
    }
)
async def create_report(
        report: ReportCreate,
        user: User = Depends(current_active_user),
        db: AsyncSession = Depends(get_async_session)):
    """Эндпоинт создания жалобы"""
    article = await services.get_article_by_id(db, report.article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with id {report.article_id} does not exist."
        )
    report = await services.create_report(db, report, user.id)
    return report


@router.get(
    '/{report_id}',
    response_model=ReportDetailRead,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Report not found"},
        status.HTTP_403_FORBIDDEN: {"description": "Forbidden"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}
    }
)
async def get_report(
        report_id: int,
        db: AsyncSession = Depends(get_async_session),
        _: User = Depends(current_active_superuser)):
    """Эндпоинт получения жалобы"""
    report = await services.get_report_with_details(db, report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report not found"
        )
    return report


@router.post(
    '/{report_id}/solve',
    response_model=ReportDetailRead,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Report not found"},
        status.HTTP_403_FORBIDDEN: {"description": "Forbidden"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}
    }
)
async def solve_report(
        report_id: int,
        db: AsyncSession = Depends(get_async_session),
        _: User = Depends(current_active_superuser)):
    """Пометить жалобу закрытой"""
    report = await services.get_report_with_details(db, report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report not found"
        )
    await services.solve_report(db, report)
    return report
