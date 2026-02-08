from base_database import BaseDatabase
from src.ventio_api.api.schema.conversation import Conversation
from datetime import datetime

class ConversationDatabase(BaseDatabase[Conversation]):
	collection_name = "converstations"
	model = Conversation

	async def get_stale_converstations(self, time_threshold: datetime.datetime) -> list[Conversation]:
		return await self.get_many(last_message_at={"$lte": time_threshold})