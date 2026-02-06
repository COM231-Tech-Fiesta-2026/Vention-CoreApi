from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

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


env = Settings(
    MONGODB_DB_NAME=str(os.getenv("MONGODB_DB_NAME")),
    MONGODB_LOCAL_URL=str(os.getenv("MONGODB_LOCAL_URL")),
)
