from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ..schemas import ReportCreate
from ..models import Report


async def get_report_by_id(
        db: AsyncSession,
        report_id: int) -> Report | None:
    """Получение жалобы по id"""
    report = await db.get(Report, report_id)
    return report


async def get_report_with_details(
        db: AsyncSession,
        report_id: int) -> Report | None:
    """Получение жалобы с подробной информацией о пользователе и статье"""
    report = await db.get(
        Report,
        report_id,
        options=[joinedload(Report.article), joinedload(Report.author)]
    )
    return report


async def list_reports(db: AsyncSession) -> Sequence[Report]:
    """Получение списка жалоб"""
    reports = await db.scalars(
        select(Report)
    )
    return reports.all()


async def create_report(
        db: AsyncSession,
        report_data: ReportCreate,
        user_id: int) -> Report:
    """Создание жалобы"""
    report = Report(**report_data.dict(), author_id=user_id)
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return report


async def solve_report(
        db: AsyncSession,
        report: Report) -> Report:
    report.solved = True
    await db.commit()
    return report
