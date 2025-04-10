from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ENV: str
    API_VERSION: str
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()