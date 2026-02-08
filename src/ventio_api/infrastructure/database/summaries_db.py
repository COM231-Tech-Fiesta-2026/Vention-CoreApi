from src.ventio_api.infrastructure.database.base_database import BaseDatabase
from ...models.summary_model import Summary
from typing import List
from uuid import UUID
from ...exceptions import ConversationNotFoundException


class SummaryDatabase(BaseDatabase[Summary]):
    collection_name = "summaries"
    model = Summary

    def __init__(self):
        super().__init__()

    async def verify_uniqueness(self, conversation_id: UUID) -> bool:
        is_unique = await self.collection.find_one({"conversation_id": conversation_id})

        if is_unique:
            return False

        return True

    async def get_summaries_by_ids(self, conversation_ids: List[UUID]) -> List[Summary]:

        try:
            cursor = self.collection.find(
                {"conversation_id": {"$in": conversation_ids}}
            ).sort("timestamp", -1)
        except ConversationNotFoundException as e:
            raise ConversationNotFoundException from e

        return [self.model(**doc) async for doc in cursor]
