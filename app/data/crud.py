from sqlalchemy.orm import Session

from app.data import models
from app.utils.logging import log
from app.dependencies import ScheduleFilters


def get_lessons(
    db: Session,
    filters: ScheduleFilters,
    offset: int,
    limit: int,
) -> list[models.Lesson]:
    """
    Получить занятия по фильтрам
    """
    db_query = db.query(models.Lesson)
    if filters.group_name:
        db_query = db_query.filter(models.Lesson.group_name == filters.group_name)
    if filters.teacher_fio:
        db_query = db_query.filter(models.Lesson.teacher_fio == filters.teacher_fio)
    if filters.room_id:
        db_query = db_query.filter(models.Lesson.room_id == filters.room_id)
    if filters.weekday is not None:
        db_query = db_query.filter(models.Lesson.weekday == filters.weekday)

    return (
        db_query.filter(models.Lesson.odd_even_week == filters.week_type)
        .offset(offset)
        .limit(limit)
        .all()
    )
