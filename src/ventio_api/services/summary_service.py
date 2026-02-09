from ..infrastructure.database.summaries_db import SummaryDatabase
from ..infrastructure.database.conversations_db import ConversationDatabase
from ..api.schema.auth import AccessTokenContent
from ..models.conversation_model import Conversation
from ..core.utils import get_now
from ..models.summary_model import Summary
from ..infrastructure.database.messages_db import MessageDatabase


class SummaryService:

    def __init__(self):
        self.summary_db = SummaryDatabase()
        self.convo_db = ConversationDatabase()
        self.message_db = MessageDatabase()

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

        llm_output: dict[str, str] = {  # mock for llm
            "title": "Malungkot si user ;(",
            "user_feelings": "Malungkot",
            "description": "Malungkot si user, umiiyak :(",
        }

        new_summary = Summary(
            conversation_id=conversation.conversation_id,
            user_id=conversation.user_id,
            title=llm_output["title"],  # change this after integrating llm
            user_feelings=llm_output[
                "user_feelings"
            ],  # change this after integrating llm
            description=llm_output["description"],  # change this after integrating llm
            timestamp=str(get_now()),
        )

        await self.summary_db.insert(new_summary)

        # deletes the messages of the conversation after summary
        await self.message_db.delete_messages_by_id(
            conversation_id=conversation.conversation_id
        )
