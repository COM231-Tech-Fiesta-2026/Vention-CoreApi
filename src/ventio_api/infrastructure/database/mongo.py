from motor.motor_asyncio import AsyncIOMotorClient
from src.ventio_api.config import env

# MongoDB connection
MONGODB_DB_NAME = env.MONGODB_DB_NAME
MONGO_LOCAL_URL = env.MONGODB_LOCAL_URL

# Create async MongoDB client
client = AsyncIOMotorClient(MONGO_LOCAL_URL, uuidRepresentation='standard')
db = client[MONGODB_DB_NAME]
