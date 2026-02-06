from uuid import UUID
from .base_database import BaseDatabase
from src.ventio_api.api.schema.conversation import Conversation


class ConversationDatabase(BaseDatabase[Conversation]):
    collection_name = "conversations"
    model = Conversation

    def __init__(self):
        super().__init__()

    async def insert_message_in_conversation(
        self, conversation_id: UUID, message_id: UUID
    ) -> Conversation:
        return await self.partial_update(
            push={"messages_ids": message_id}, conversation_id=conversation_id
        )
