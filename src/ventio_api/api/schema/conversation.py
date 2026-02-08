from pydantic import BaseModel, Field
from typing import Literal, Optional, List
from uuid import UUID
from ...models.message_model import Message


class ConversationInput(BaseModel):
    mode: Literal["vent", "advice"] = Field(...)
    conversation_key: Optional[UUID] = None
    content: str = Field(...)


class ConversationOutput(BaseModel):
    conversation_id: UUID = Field(...)
    reply: str = Field(...)


class ConversationHistory(BaseModel):
    conversation_id: UUID = Field(...)
    messages: List[Message] = Field(...)
