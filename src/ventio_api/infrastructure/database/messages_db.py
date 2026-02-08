from .base_database import BaseDatabase
from ...models.message_model import Message
from typing import List
from uuid import UUID
from ...exceptions import MessageNotFoundException


class MessageDatabase(BaseDatabase[Message]):
    collection_name = "messages"
    model = Message

    def __init__(self):
        super().__init__()

    async def get_messages_by_ids(self, message_ids: List[UUID]) -> List[Message]:
        try:
            messages = self.collection.find({"message_id": {"$in": message_ids}})
        except MessageNotFoundException as e:
            raise MessageNotFoundException from e

        return [self.model(**doc) async for doc in messages]

    async def delete_messages_after_summary(self, conversation_id: UUID) -> None:
        result = await self.delete(conversation_id=conversation_id)

        if not result:
            raise MessageNotFoundException(
                f"No messages found to delete for conversation {conversation_id}"
            )
