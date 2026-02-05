from typing import Dict
from ..infrastructure.database.messages_db import MessageDatabase
from ..infrastructure.database.conversations_db import ConversationDatabase
from ..api.schema.conversation import Conversation
from ..api.schema.message import Message
from ..exceptions import NotFoundException, CoreApiException, DatabaseException
from fastapi.exceptions import HTTPException
from uuid import uuid4
from datetime import datetime, UTC
from seeders.seed_users import get_seed_users


class ConversationService:

    def __init__(self):
        self.convo_db = ConversationDatabase()
        self.message_db = MessageDatabase()
        self.now = datetime.now(UTC)

    async def handle_conversation_service(self, payload: Dict) -> Dict:

        if payload["conversation_key"]:
            res = await self.update_conversation_service(payload)
        else:
            res = await self.create_conversation_service(payload)
        return res

    async def create_conversation_service(self, payload: Dict):
        try:

            self.user = await get_seed_users()  # hardcoded for now
            conversation = await self.convo_db.insert(
                Conversation(
                    user_id=self.user["user_id"],
                    conversation_id=str(uuid4()),
                    messages_ids=[],
                    has_ended=False,
                    last_message_timestamp=str(self.now),
                )
            )

            message = await self.message_db.insert(
                Message(
                    message_id=str(uuid4()),
                    conversation_id=conversation.conversation_id,
                    content=payload["content"],
                    sender_name=self.user["name"],
                    timestamp=str(self.now),
                )
            )

            await self.convo_db.insert_message_in_conversation(
                conversation_id=conversation.conversation_id,
                message_id=message.message_id,
            )

            return {
                "conversation_id": conversation.conversation_id,
                "reply": "Okay lang yannnn",  # hardcoded for now
            }
        except CoreApiException:
            # Re-raise custom exceptions so the Global Handler catches them
            raise
        except Exception as e:
            # Catch unexpected Python errors and wrap them
            raise DatabaseException(
                message="An unexpected error occurred while creating the conversation.",
                debug_info=repr(e),  # This will be hidden in Prod but visible in Dev
            )

    async def update_conversation_service(self, payload: Dict):
        pass

    async def end_conversation_service(self, conversation_id):
        pass
