from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    MONGODB_LOCAL_URL: str
    MONGODB_DB_NAME: str

    # SECRET_KEY: str
    # ALGORITHM: str
    # ACCESS_TOKEN_EXPIRE_MINUTES: int

    # LLM_API_KEY: str
    # LLM_ENDPOINT: str

    class Config:
        env_file = ".env"


env = Settings()
