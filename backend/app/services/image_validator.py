from dataclasses import dataclass
from io import BytesIO

from PIL import Image, UnidentifiedImageError

SUPPORTED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


class ImageValidationError(Exception):
    """Custom exception for image validation errors."""


@dataclass(frozen=True)
class ValidatedImage:
    """Dataclass to hold validated image data."""

    filename: str
    content_type: str
    size_bytes: int


def validate_image(
    image_bytes: bytes,
    filename: str,
    content_type: str | None,
    max_size_bytes: int,
) -> ValidatedImage:
    if not image_bytes:
        raise ImageValidationError("Uploaded image is empty.")

    if len(image_bytes) > max_size_bytes:
        raise ImageValidationError("Uploaded image exceeds the maximum size.")

    if content_type not in SUPPORTED_MIME_TYPES:
        raise ImageValidationError("Unsupported image type.")

    try:
        with Image.open(BytesIO(image_bytes)) as image:
            image.verify()
    except (UnidentifiedImageError, OSError) as err:
        raise ImageValidationError("Uploaded file is not a valid image.") from err

    return ValidatedImage(
        filename=filename, content_type=content_type, size_bytes=len(image_bytes)
    )
