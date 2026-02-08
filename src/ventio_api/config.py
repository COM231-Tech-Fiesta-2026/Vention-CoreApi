from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_LOCAL_URL: str
    MONGODB_DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 120

    LLM_API_KEY: str
    LLM_ENDPOINT: str

    class Config:
        env_file = ".env"


env = Settings()
