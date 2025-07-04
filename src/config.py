from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_ID: str
    API_HASH: str

    TELEGRAM_CHANNELS_IDS: list[int]

    PHONE_NUMBER: str

    TELEGRAM_BOT_TOKEN: str

    TELEGRAM_ADMIN_ID: int

    LLM_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()