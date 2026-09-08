from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.core.config import get_settings
from app.schemas.menu import Menu
from app.services.dependencies import (
    get_vision_service,
    get_drink_image_service,
)
from app.services.image_validator import (
    ImageValidationError,
    validate_image,
)
from app.services.vision import VisionService
from app.services.drink_images.service import DrinkImageService

router = APIRouter()

settings = get_settings()


@router.post("/scan", response_model=Menu)
async def scan_menu(
    image: UploadFile = File(...),
    vision_service: VisionService = Depends(get_vision_service),
    drink_image_service: DrinkImageService = Depends(get_drink_image_service),
) -> Menu:
    try:
        image_bytes = await image.read()

        validate_image(
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

    # return await vision_service.extract_menu(
    #     image_bytes, content_type=image.content_type
    # )
    menu = await vision_service.extract_menu(
        image=image_bytes, content_type=image.content_type
    )

    for item in menu.items:
        image_path = drink_image_service.find_image(item.name)

        if image_path is not None:
            item.image_url = f"/drink-images/{image_path.name}"
    return menu
