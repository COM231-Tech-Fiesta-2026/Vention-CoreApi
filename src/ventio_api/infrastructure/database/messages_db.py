from .base_database import BaseDatabase
from ...models.message_model import Message
from typing import List
from uuid import UUID
from ...exceptions import MessageNotFoundException
from ...api.schema.message import MessageContext


class MessageDatabase(BaseDatabase[Message]):
    collection_name = "messages"
    model = Message

    def __init__(self):
        super().__init__()

    async def get_messages_by_ids(self, message_ids: List[UUID]) -> List[Message]:
        cursor = self.collection.find({"message_id": {"$in": message_ids}})
        docs = [doc async for doc in cursor]

        if len(docs) != len(message_ids):
            raise MessageNotFoundException("One or more messages does not exists.")

        return [self.model(**doc) for doc in docs]

    async def delete_messages_by_id(self, conversation_id: UUID) -> None:
        result = await self.delete(conversation_id=conversation_id)

        if not result:
            raise MessageNotFoundException(
                f"No messages found to delete for conversation {conversation_id}"
            )

    async def get_messages_by_id(self, conversation_id: UUID) -> list[MessageContext]:
        projection = {"content": 1, "reply": 1, "_id": 0}

        cursor = self.collection.find({"conversation_id": conversation_id}, projection)

        # Returning as a list of dictionaries
        return [MessageContext(**doc) async for doc in cursor]
