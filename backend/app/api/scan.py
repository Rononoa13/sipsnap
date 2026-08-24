from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.config import get_settings
from app.services.image_validator import (
    ImageValidationError,
    validate_image,
)

router = APIRouter()

settings = get_settings()


@router.post("/scan")
async def scan_menu(
    image: UploadFile = File(...),
) -> dict[str, str | int]:
    try:
        image_bytes = await image.read()

        validated_image = validate_image(
            image_bytes=image_bytes,
            filename=image.filename or "unknown",
            content_type=image.content_type,
            max_size_bytes=settings.max_image_size_bytes,
        )
    except ImageValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return {
        "filename": validated_image.filename,
        "content_type": validated_image.content_type,
        "size_bytes": validated_image.size_bytes,
    }
