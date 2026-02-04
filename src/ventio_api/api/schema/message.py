from pydantic import BaseModel, Field
from uuid import UUID

class Message(BaseModel):
	message_id: UUID = Field(...)
	converstation_id: UUID = Field(...)
	sender_name: str = Field(...)
	timestamp: str = Field(...)