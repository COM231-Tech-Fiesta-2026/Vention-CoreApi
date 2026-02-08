from ..infrastructure.database.summaries_db import SummaryDatabase
from ..infrastructure.database.conversations_db import ConversationDatabase
from ..api.schema.auth import AccessTokenContent


class SummaryService:

    def __init__(self):
        self.summary_db = SummaryDatabase()
        self.convo_db = ConversationDatabase()

    async def get_history(self, token: AccessTokenContent):
        conversations = await self.convo_db.get_latest_conversation(
            user_id=token.user_id, limit=3
        )
        conversation_ids = [convo.conversation_id for convo in conversations]

        summaries = await self.summary_db.get_summaries_by_ids(
            conversation_ids=conversation_ids
        )

        return summaries
