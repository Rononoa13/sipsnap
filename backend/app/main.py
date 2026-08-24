import logging

from fastapi import FastAPI

from app.api.scan import router as scan_router
from app.core.config import get_settings

settings = get_settings()

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name)

app.include_router(scan_router, prefix="/api")


@app.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint to verify that the application is running.
    """
    logger.info("Health check performed")
    return {"status": "ok"}
