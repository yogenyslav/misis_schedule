from fastapi import APIRouter
import app.routers.schedule as schedule

router = APIRouter(prefix="/api")
router.include_router(schedule.router)
