from pydantic import BaseModel, Field
from uuid import UUID

class Summary(BaseModel):
	conversation_id: UUID = Field(...)
	title: str = Field(...)
	content: str = Field(...)
	timestamp: str = Field(...)