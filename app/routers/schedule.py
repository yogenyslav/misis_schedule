import datetime
from typing import Annotated

from fastapi import (
    APIRouter,
    UploadFile,
    Depends,
    status,
    Response,
    HTTPException,
    Query,
)
from sqlalchemy.orm import Session

from app.data import schemas
from app.utils.logging import log
from app.utils.upload import upload_schedules  # , upload_schedules_ibo
from app.data import crud
from app.dependencies import get_db, ScheduleFilters


router = APIRouter(prefix="/schedule", tags=["schedule"])


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
)
async def upload_schedule():
    """
    Загрузить расписание в формате Excel
    """
    # try:
    #     upload_schedules()
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f"Error while uploading schedules: {e}",
    #     )

    upload_schedules()
    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/", response_model=list[schemas.LessonDto] | None)
async def get_schedule(
    filters: ScheduleFilters = Depends(ScheduleFilters),
    db: Session = Depends(get_db),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
) -> list[schemas.LessonDto] | None:
    """
    Получить расписание по фильтрам
    """
    log.debug(filters)
    if not filters():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must specify at least one filter",
        )

    filters.weekday: int | None = None
    filters.week_type: int = datetime.date.today().isocalendar()[1] % 2
    if filters.date:
        filters.weekday = filters.date.weekday()
        filters.week_type = filters.date.isocalendar()[1] % 2

    log.debug(f"weekday={filters.weekday} week_type={filters.week_type}")
    db_lessons = crud.get_lessons(db, filters, offset, limit)
    return db_lessons
