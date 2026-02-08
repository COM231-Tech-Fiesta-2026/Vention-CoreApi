from pydantic import BaseModel, Field
from uuid import UUID


class Summary(BaseModel):
    conversation_id: UUID = Field(...)
    user_id: UUID = Field(...)
    title: str = Field(...)
    user_feelings: str = Field(...)
    description: str = Field(...)
    timestamp: str = Field(...)
