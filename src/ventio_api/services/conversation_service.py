from ..infrastructure.database.messages_db import MessageDatabase
from ..infrastructure.database.conversations_db import ConversationDatabase
from ..api.schema.conversation import (
    Conversation,
    ConversationOutput,
    ConversationInput,
)
from ..api.schema.message import Message
from ..exceptions import (
    DatabaseException,
    NotFoundException,
    UserNotFoundException,
    ConversationNotFoundException,
)
from typing import List
from uuid import uuid4, UUID
from datetime import datetime, UTC
from seeders.seed_users import get_seed_users


class ConversationService:

    def __init__(self):
        self.convo_db = ConversationDatabase()
        self.message_db = MessageDatabase()
        self.now = datetime.now(UTC)

    async def process_message(
        self, conversation_input: ConversationInput
    ) -> ConversationOutput:

        if conversation_input.conversation_key:
            res = await self.update(conversation_input)
        else:
            res = await self.create(conversation_input)
        return res

    async def create(self, conversation_input: ConversationInput) -> ConversationOutput:

        try:
            self.user = await get_seed_users()  # hardcoded for now
        except Exception as e:
            raise UserNotFoundException(
                message="Failed to fetch seed user data.", debug_info=str(e)
            )

        if not self.user:
            raise UserNotFoundException(
                "Required user record is missing from seed data."
            )

        new_conversation = Conversation(
            user_id=self.user.user_id,
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
            sender_name=self.user.name,
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

    async def update(self, conversation_input: ConversationInput) -> ConversationOutput:

        try:
            self.user = await get_seed_users()
        except Exception as e:
            raise UserNotFoundException(
                message="Failed to retrieve user context for update.", debug_info=str(e)
            )

        if not self.user:
            raise UserNotFoundException(message="User session not found.")
        conversation_key = conversation_input.conversation_key

        if not conversation_key:  # must be added, because type safety requires it.
            raise ConversationNotFoundException(
                "Conversation_key is required to update conversation."
            )

        new_message = Message(
            message_id=uuid4(),
            conversation_id=conversation_key,
            content=conversation_input.content,
            sender_name=self.user.name,
            timestamp=str(self.now),
        )
        message = await self.message_db.insert(new_message)

        try:
            await self.convo_db.insert_message_in_conversation(
                conversation_id=conversation_key,
                message_id=message.message_id,
            )
        except NotFoundException as e:
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

    async def get(self, user_id: UUID) -> List[Conversation]:

        conversations = await self.convo_db.get_many(user_id=user_id)

        return conversations
