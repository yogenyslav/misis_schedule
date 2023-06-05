from fastapi import FastAPI

from app.data import models
from app.data.db import engine
from app.routers import router


async def on_startup():
    models.Base.metadata.create_all(bind=engine)


def create_app():
    app = FastAPI()
    app.add_event_handler("startup", on_startup)

    app.include_router(router)
    return app
