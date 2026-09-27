from typing import Type, TypeVar

from google import genai
from google.genai import types
from pydantic import BaseModel

from .config import get_settings


T = TypeVar("T", bound=BaseModel)


class GeminiService:

    def __init__(self):

        settings = get_settings()

        if not settings.effective_api_key:
            raise RuntimeError(
                "Gemini API key is missing. "
                "Add GEMINI_API_KEY to your .env file."
            )

        self.settings = settings

        self.client = genai.Client(
            api_key=settings.effective_api_key
        )

    def generate_text(self, prompt: str) -> str:

        response = self.client.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(
                    thinking_level=self.settings.gemini_thinking_level
                )
            ),
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return response.text.strip()

    def generate_structured(
        self,
        prompt: str,
        schema: Type[T]
    ) -> T:

        response = self.client.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema,
                thinking_config=types.ThinkingConfig(
                    thinking_level=self.settings.gemini_thinking_level
                ),
            ),
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty structured response."
            )

        return schema.model_validate_json(
            response.text
        )


def get_gemini_service() -> GeminiService:

    return GeminiService()