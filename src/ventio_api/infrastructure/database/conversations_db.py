from base_database import BaseDatabase
from src.ventio_api.api.schema.conversation import Conversation

class ConversationDatabase(BaseDatabase[Conversation]):
	collection_name = "converstations"
	model = Conversation