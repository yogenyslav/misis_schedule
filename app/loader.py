import datetime

from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from app.data import models
from app.data.db import engine
from app.routers import router
from app.utils.upload import upload_schedules

scheduler = BackgroundScheduler(timezone="Europe/Moscow")


async def on_startup():
    models.Base.metadata.create_all(bind=engine)

    scheduler.start()
    scheduler.add_job(
        upload_schedules,
        trigger="interval",
        seconds=86400,
        next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=15),
    )


def create_app():
    app = FastAPI()
    app.add_event_handler("startup", on_startup)

    app.include_router(router)
    return app
