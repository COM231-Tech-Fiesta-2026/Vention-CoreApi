from src.ventph_api.infrastructure.database.base_database import BaseDatabase
from src.ventph_api.api.schema.message import Message

class MessageDatabase(BaseDatabase[Message]):
	collection_name = "messages"
	model = Message

user_db = MessageDatabase()