from .base_database import BaseDatabase
from src.ventio_api.api.schema.conversation import Conversation


class ConversationDatabase(BaseDatabase[Conversation]):
    collection_name = "conversations"
    model = Conversation

    def __init__(self):
        super().__init__()

    async def insert_message_in_conversation(self, conversation_id, message_id):
        return await self.partial_update(
            push={"messages_id": message_id}, conversation_id=conversation_id
        )
