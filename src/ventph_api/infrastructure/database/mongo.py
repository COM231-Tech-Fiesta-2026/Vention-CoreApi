from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")
MONGO_URL = os.getenv("MONGO_LOCAL_URL")

client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGODB_DB_NAME]

users_collection = db["users"]