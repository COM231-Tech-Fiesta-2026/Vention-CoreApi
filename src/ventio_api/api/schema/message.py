from pydantic import BaseModel, Field


class MessageContext(BaseModel):
    content: str = Field(...)
    reply: str = Field(...)
