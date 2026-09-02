from google import genai
from google.genai import types

from app.schemas.gemini_schema import make_gemini_schema
from app.schemas.menu import Menu
from app.services.vision import VisionProviderError, VisionService


class GeminiVisionService(VisionService):
    def __init__(self, api_key: str, model: str) -> None:
        print("Gemini API key exists:", bool(api_key))
        print("Gemini API key length:", len(api_key))
        print("Gemini API key prefix:", api_key[:5] if api_key else None)
        self.client = genai.Client(api_key=api_key)
        self.model = model

    async def extract_menu(self, image: bytes, content_type: str) -> Menu:
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=[
                    types.Part.from_bytes(
                        data=image,
                        mime_type=content_type,
                    ),
                    "Extract all menu items from this image.",
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=make_gemini_schema(Menu),
                ),
            )
            return Menu.model_validate(response.parsed)
        except Exception as e:
            raise VisionProviderError(f"Failed to extract menu: {str(e)}") from e
