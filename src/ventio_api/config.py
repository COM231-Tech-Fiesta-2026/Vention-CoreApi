from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGODB_LOCAL_URL: str
    MONGODB_DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 120

    # LLM_API_KEY: str
    # LLM_ENDPOINT: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",        # Fixes the "Extra inputs are not permitted" crash
        case_sensitive=False   # Fixes "mongo_local_url" vs "MONGODB_LOCAL_URL" mismatch
    )

settings = Settings()