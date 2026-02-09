from uuid import UUID
from .base_database import BaseDatabase
from ...models.conversation_model import Conversation
import datetime
from typing import List
from ...exceptions import InvalidStateTransitionException, ConversationNotFoundException


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

        conversations = (
            self.collection.find({"user_id": user_id, "has_ended": True})
            .sort("last_message_timestamp", -1)
            .limit(limit)
        )
        return [self.model(**doc) async for doc in conversations]

    async def get_stale_conversations(
        self, time_threshold: datetime.datetime
    ) -> list[Conversation]:
        return await self.get_many(last_message_at={"$lte": time_threshold})

    async def end_conversation(self, conversation_id: UUID) -> Conversation:
        conversation = await self.collection.find_one(
            {"conversation_id": conversation_id},
            {"has_ended": 1, "_id": 0},
        )
        if not conversation:
            raise ConversationNotFoundException(
                f"No conversation found with ID {conversation_id}"
            )

        if conversation["has_ended"]:
            raise InvalidStateTransitionException("This conversation is already ended.")

        try:
            return await self.partial_update(
                set={"has_ended": True}, conversation_id=conversation_id
            )
        except ConversationNotFoundException as e:
            raise ConversationNotFoundException from e
