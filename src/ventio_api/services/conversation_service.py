from ..infrastructure.database.messages_db import MessageDatabase
from ..infrastructure.database.conversations_db import ConversationDatabase
from ..api.schema.conversation import (
    Conversation,
    ConversationOutput,
    ConversationInput,
    ConversationHistory,
)
from ..api.schema.auth import AccessTokenContent
from ..api.schema.message import Message
from ..exceptions import (
    DatabaseException,
    NotFoundException,
    ConversationNotFoundException,
)
from typing import List
from uuid import uuid4, UUID
from datetime import datetime, UTC


class ConversationService:

    def __init__(self):
        self.convo_db = ConversationDatabase()
        self.message_db = MessageDatabase()
        self.now = datetime.now(UTC)

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
            messages_ids=[],
            has_ended=False,
            last_message_timestamp=str(self.now),
        )
        conversation = await self.convo_db.insert(new_conversation)

        new_message = Message(
            message_id=uuid4(),
            conversation_id=conversation.conversation_id,
            content=conversation_input.content,
            reply="Okay lang yannnn",
            sender_name=token.name,
            timestamp=str(self.now),
        )
        message = await self.message_db.insert(new_message)

        await self.convo_db.insert_message_in_conversation(
            conversation_id=conversation.conversation_id,
            message_id=message.message_id,
        )

        return ConversationOutput(
            conversation_id=conversation.conversation_id,
            reply="Okay lang yannnn",  # hardcoded for now
        )

    async def update(
        self, conversation_input: ConversationInput, token: AccessTokenContent
    ) -> ConversationOutput:

        conversation_key = conversation_input.conversation_key

        if not conversation_key:  # must be added, because type safety requires it.
            raise ConversationNotFoundException(
                "Conversation_key is required to update conversation."
            )

        new_message = Message(
            message_id=uuid4(),
            conversation_id=conversation_key,
            content=conversation_input.content,
            reply="Okay lang yannn!",
            sender_name=token.name,
            timestamp=str(self.now),
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

        return ConversationOutput(
            conversation_id=conversation_key,
            reply="Okay lang yannn",  # Hardcoded for now
        )

    async def close(self, conversation_id: UUID) -> None:

        try:
            await self.convo_db.partial_update(
                set={"has_ended": True}, conversation_id=conversation_id
            )
        except DatabaseException as e:
            raise DatabaseException(
                message=("Failed to end conversation."), debug_info=(str(e))
            )

    async def get(self, token: AccessTokenContent) -> List[ConversationHistory]:
        conversations = await self.convo_db.get_many(user_id=token.user_id)
        result: List[ConversationHistory] = []

        for convo in conversations:
            current_convo_messages: List[str] = []

            for m_id in convo.messages_ids:
                msg_doc = await self.message_db.get_content(m_id)
                if msg_doc and "content" in msg_doc:
                    current_convo_messages.append(msg_doc["content"])

            result.append(
                ConversationHistory(
                    conversation_id=convo.conversation_id,
                    content=current_convo_messages,
                )
            )

        return result
