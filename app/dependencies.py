import datetime

from app.data.db import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ScheduleFilters:
    def __init__(
        self,
        group_name: str | None = None,
        teacher_fio: str | None = None,
        room_id: str | None = None,
        date: datetime.date | None = None,
    ):
        self.group_name = group_name
        self.teacher_fio = teacher_fio
        self.room_id = room_id
        self.date = date

    def __call__(self):
        return self.group_name or self.teacher_fio or self.room_id

    def __repr__(self) -> str:
        return f"<ScheduleFilters group_name={self.group_name} teacher_fio={self.teacher_fio} room_id={self.room_id} date={self.date}>"
