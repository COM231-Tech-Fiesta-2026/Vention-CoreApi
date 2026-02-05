from pydantic import BaseModel, Field
from enum import Enum
from typing import Literal, Optional
from uuid import UUID


class Conversation(BaseModel):
    user_id: UUID = Field(...)
    conversation_id: UUID = Field(...)
    messages_ids: list[UUID] = Field(...)
    has_ended: bool = Field(...)
    last_message_timestamp: str = Field(...)


class ConversationInput(BaseModel):
    mode: Literal["vent", "advice"] = Field(...)
    conversation_key: Optional[UUID] = None
    content: str = Field(...)
