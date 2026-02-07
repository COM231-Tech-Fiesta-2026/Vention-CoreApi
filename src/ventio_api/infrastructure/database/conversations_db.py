from uuid import UUID
from .base_database import BaseDatabase
from ...models.conversation_model import Conversation
from typing import List


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

    async def get_latest_conversation(
        self, user_id: UUID, limit: int = 0
    ) -> List[Conversation]:

        conversations = self.collection.find({"user_id": user_id}).limit(limit)
        return [self.model(**doc) async for doc in conversations]
