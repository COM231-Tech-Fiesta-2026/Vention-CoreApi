from src.ventio_api.infrastructure.database.base_database import BaseDatabase
from src.ventio_api.api.schema.message import Message
from typing import List
from uuid import UUID
from ...exceptions import NotFoundException


class MessageDatabase(BaseDatabase[Message]):
    collection_name = "messages"
    model = Message

    def __init__(self):
        super().__init__()

    async def get_messages_by_ids(self, message_ids: List[UUID]) -> List[Message]:
        try:
            messages = self.collection.find({"message_id": {"$in": message_ids}})
        except NotFoundException as e:
            raise NotFoundException from e

        return [self.model(**doc) async for doc in messages]
