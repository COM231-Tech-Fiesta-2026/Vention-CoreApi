from pydantic import BaseModel, Field
from enum import Enum
from uuid import UUID


class Converstation(BaseModel):
    user_id: UUID = Field(...)
    converstation_id: UUID = Field(...)
    messages_ids: list[UUID] = Field(...)
    has_ended: bool = Field(...)
    last_message_timestamp: str = Field(...)


class ConversationMode(Enum):
    vent = "vent"
    advice = "advice"
