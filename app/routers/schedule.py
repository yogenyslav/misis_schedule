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
from app.utils.schedule import upload_schedules, upload_schedules_ibo
from app.data import crud
from app.dependencies import get_db, ScheduleFilters


router = APIRouter(prefix="/schedule", tags=["schedule"])


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
)
async def upload_schedule(file: UploadFile):
    """
    Загрузить расписание в формате Excel
    """
    log.debug(f"Uploading schedules: {file.filename}")
    try:
        if "ibo" not in file.filename:
            upload_schedules(file)
        else:
            raise NotImplementedError
            # upload_schedules_ibo(file)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error while uploading schedules: {e}",
        )
    log.debug("Schedules uploaded")

    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/", response_model=list[schemas.LessonDto] | None)
async def get_schedule(
    filters: Annotated[ScheduleFilters, Depends()],
    db: Annotated[Session, Depends(get_db)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
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
