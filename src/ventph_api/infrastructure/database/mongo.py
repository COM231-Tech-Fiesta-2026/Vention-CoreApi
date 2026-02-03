from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MongoDB connection
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")
MONGO_LOCAL_URL = os.getenv("MONGO_LOCAL_URL")

# Create async MongoDB client
client = AsyncIOMotorClient(MONGO_LOCAL_URL)
db = client[MONGODB_DB_NAME]
