from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer

from app.data.db import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[str] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)
    weekday: Mapped[int] = mapped_column(Integer)
    order: Mapped[int] = mapped_column(Integer)
    odd_even_week: Mapped[int] = mapped_column(Integer)
    type: Mapped[str] = mapped_column(String, nullable=True)

    group_name: Mapped[str] = mapped_column(String, index=True)
    teacher_fio: Mapped[str] = mapped_column(String, index=True, nullable=True)
    room_id: Mapped[str] = mapped_column(String, index=True)
