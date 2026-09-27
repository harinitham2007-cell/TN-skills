from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Gemini API
    gemini_api_key: str = ""
    google_api_key: str = ""

    # Gemini 3.8 Flash
    gemini_model: str = "gemini-3.8-flash"
    gemini_thinking_level: str = "medium"

    # FastAPI
    app_host: str = "127.0.0.1"
    app_port: int = 8000

    # Optional local explanation model
    use_local_explainer: bool = False
    local_model_name: str = "MBZUAI/LaMini-Flan-T5-783M"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @property
    def effective_api_key(self) -> str:
        return self.gemini_api_key or self.google_api_key


@lru_cache
def get_settings() -> Settings:
    return Settings()