from src.ventio_api.infrastructure.database.base_database import BaseDatabase
from src.ventio_api.api.schema.message import Message
from uuid import UUID
from ...exceptions import NotFoundException


class MessageDatabase(BaseDatabase[Message]):
    collection_name = "messages"
    model = Message

    def __init__(self):
        super().__init__()

    async def get_content(self, message_id: UUID):
        try:
            return await self.collection.find_one(
                {"message_id": message_id}, {"content": 1, "_id": 0}
            )
        except NotFoundException as e:
            raise NotFoundException from e
