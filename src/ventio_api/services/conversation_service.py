from ..infrastructure.database.messages_db import MessageDatabase
from ..infrastructure.database.conversations_db import ConversationDatabase
from ..api.schema.conversation import (
    Conversation,
    ConversationOutput,
    ConversationInput,
    EndConversationInput,
)
from ..api.schema.message import Message
from ..exceptions import DatabaseException
from uuid import uuid4
from datetime import datetime, UTC
from seeders.seed_users import get_seed_users


class ConversationService:

    def __init__(self):
        self.convo_db = ConversationDatabase()
        self.message_db = MessageDatabase()
        self.now = datetime.now(UTC)

    async def handle_conversation_service(
        self, conversation_input: ConversationInput
    ) -> ConversationOutput:

        if conversation_input.conversation_key:
            res = await self.update_conversation_service(conversation_input)
        else:
            res = await self.create_conversation_service(conversation_input)
        return res

    async def create_conversation_service(
        self, conversation_input: ConversationInput
    ) -> ConversationOutput:
        try:

            self.user = await get_seed_users()  # hardcoded for now
            conversation_load = Conversation(
                user_id=self.user.user_id,
                conversation_id=uuid4(),
                messages_ids=[],
                has_ended=False,
                last_message_timestamp=str(self.now),
            )
            conversation = await self.convo_db.insert(conversation_load)

            message = await self.message_db.insert(
                Message(
                    message_id=uuid4(),
                    conversation_id=conversation.conversation_id,
                    content=conversation_input.content,
                    sender_name=self.user.name,
                    timestamp=str(self.now),
                )
            )

            await self.convo_db.insert_message_in_conversation(
                conversation_id=conversation.conversation_id,
                message_id=message.message_id,
            )

            return ConversationOutput(
                conversation_id=conversation.conversation_id,
                reply="Okay lang yannnn",  # hardcoded for now
            )

        except Exception as e:
            raise DatabaseException(
                message="An unexpected error occurred while creating the conversation.",
                debug_info=repr(e),  # This will be hidden in Prod but visible in Dev
            )

    async def update_conversation_service(
        self, conversation_input: ConversationInput
    ) -> ConversationOutput:

        self.user = await get_seed_users()  # hardcoded for now
        conversation_key = conversation_input.conversation_key

        if not conversation_key:
            raise ValueError("conversation_key is required to update conversation.")

        message = await self.message_db.insert(
            Message(
                message_id=uuid4(),
                conversation_id=conversation_key,
                content=conversation_input.content,
                sender_name=self.user.name,
                timestamp=str(self.now),
            )
        )

        await self.convo_db.insert_message_in_conversation(
            conversation_id=conversation_key,
            message_id=message.message_id,
        )

        return ConversationOutput(
            conversation_id=conversation_key,
            reply="Okay lang yannn",  # Hardcoded for now
        )

    async def end_conversation_service(
        self, conversation_id: EndConversationInput
    ) -> None:
        pass
