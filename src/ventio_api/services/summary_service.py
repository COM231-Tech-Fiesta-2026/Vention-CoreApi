from ..infrastructure.database.summaries_db import SummaryDatabase
from ..infrastructure.database.conversations_db import ConversationDatabase
from ..api.schema.auth import AccessTokenContent
from ..models.conversation_model import Conversation
from ..core.utils import get_now
from ..models.summary_model import Summary
from ..infrastructure.database.messages_db import MessageDatabase
from .llm_service import LLMService


class SummaryService:

    def __init__(self):
        self.summary_db = SummaryDatabase()
        self.convo_db = ConversationDatabase()
        self.message_db = MessageDatabase()
        self.llm_service = LLMService()

    async def get_summaries(self, token: AccessTokenContent) -> list[Summary]:
        conversations = await self.convo_db.get_latest_conversation(
            user_id=token.user_id, limit=3
        )
        conversation_ids = [convo.conversation_id for convo in conversations]

        summaries = await self.summary_db.get_summaries_by_ids(
            conversation_ids=conversation_ids
        )

        return summaries

    async def summarize_conversations(self, conversation: Conversation):

        summary = await self.llm_service.summarize(
            conversation_id=conversation.conversation_id
        )

        new_summary = Summary(
            conversation_id=conversation.conversation_id,
            user_id=conversation.user_id,
            title=summary.title,
            user_feelings=summary.user_feelings,
            description=summary.description,
            timestamp=str(get_now()),
        )

        await self.summary_db.insert(new_summary)

        # deletes the messages of the conversation after summary
        await self.message_db.delete_messages_by_id(
            conversation_id=conversation.conversation_id
        )
