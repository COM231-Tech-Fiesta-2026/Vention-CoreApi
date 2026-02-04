from motor.motor_asyncio import AsyncIOMotorClient
from src.ventio_api.config import settings

# MongoDB connection
MONGODB_DB_NAME = settings.MONGODB_DB_NAME
MONGO_LOCAL_URL = settings.MONGODB_LOCAL_URL

# Create async MongoDB client
client = AsyncIOMotorClient(MONGO_LOCAL_URL, uuidRepresentation='standard')
db = client[MONGODB_DB_NAME]
