from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class Message(BaseModel):
    message_id: UUID = Field(...)
    conversation_id: UUID = Field(...)
    content: str = Field(...)
    reply: Optional[str] = None
    sender_name: str = Field(...)
    timestamp: str = Field(...)
