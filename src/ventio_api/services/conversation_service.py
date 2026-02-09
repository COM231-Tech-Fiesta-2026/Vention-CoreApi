from ..infrastructure.database.messages_db import MessageDatabase
from ..infrastructure.database.conversations_db import ConversationDatabase
from ..api.schema.conversation import (
    ConversationOutput,
    ConversationInput,
)
from ..api.schema.auth import AccessTokenContent
from ..exceptions import (
    NotFoundException,
    ConversationNotFoundException,
    LLMConnectionException,
)
from uuid import uuid4, UUID
from ..models.conversation_model import Conversation
from ..models.message_model import Message
from ..infrastructure.database.summaries_db import SummaryDatabase
from .summary_service import SummaryService
from .llm_service import LLMService
from ..core.utils import get_now


class ConversationService:

    def __init__(self):
        self.convo_db = ConversationDatabase()
        self.message_db = MessageDatabase()
        self.summary_db = SummaryDatabase()
        self.summary_service = SummaryService()
        self.llm_service = LLMService()

    async def process_message(
        self, conversation_input: ConversationInput, token: AccessTokenContent
    ) -> ConversationOutput:

        if conversation_input.conversation_key:
            res = await self.update(conversation_input, token)
        else:
            res = await self.create(conversation_input, token)
        return res

    async def create(
        self, conversation_input: ConversationInput, token: AccessTokenContent
    ) -> ConversationOutput:

        new_conversation = Conversation(
            user_id=token.user_id,
            conversation_id=uuid4(),
            mode=conversation_input.mode,
            messages_ids=[],
            has_ended=False,
            last_message_timestamp=str(get_now()),
        )
        conversation = await self.convo_db.insert(new_conversation)

        updated_input = conversation_input.model_copy(
            update={"conversation_key": conversation.conversation_id}
        )

        reply = await self.llm_service.ask_llm(updated_input)

        if not reply:
            raise LLMConnectionException

        new_message = Message(
            message_id=uuid4(),
            conversation_id=conversation.conversation_id,
            content=conversation_input.content,
            reply=reply,
            sender_name=token.name,
            timestamp=str(get_now()),
        )
        message = await self.message_db.insert(new_message)

        await self.convo_db.insert_message_in_conversation(
            conversation_id=conversation.conversation_id,
            message_id=message.message_id,
        )

        return ConversationOutput(
            conversation_id=conversation.conversation_id, reply=reply
        )

    async def update(
        self, conversation_input: ConversationInput, token: AccessTokenContent
    ) -> ConversationOutput:

        conversation_key = conversation_input.conversation_key

        if not conversation_key:  # must be added, because type safety requires it.
            raise ConversationNotFoundException(
                "Conversation_key is required to update conversation."
            )

        reply = await self.llm_service.ask_llm(conversation_input)

        new_message = Message(
            message_id=uuid4(),
            conversation_id=conversation_key,
            content=conversation_input.content,
            reply=reply,
            sender_name=token.name,
            timestamp=str(get_now()),
        )
        message = await self.message_db.insert(new_message)

        try:
            await self.convo_db.insert_message_in_conversation(
                conversation_id=conversation_key,
                message_id=message.message_id,
            )
        except NotFoundException:
            raise ConversationNotFoundException(
                message=f"Conversation with ID {conversation_key} was not found.",
                debug_info=f"Linked message_id: {message.message_id}",
            )

        return ConversationOutput(conversation_id=conversation_key, reply=reply)

    async def end(self, conversation_id: UUID) -> None:

        conversation = await self.convo_db.end_conversation(
            conversation_id=conversation_id
        )

        if await self.summary_db.verify_uniqueness(conversation_id):
            await self.summary_service.summarize_conversations(
                conversation=conversation
            )
