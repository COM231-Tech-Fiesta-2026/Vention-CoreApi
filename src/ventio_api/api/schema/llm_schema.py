from pydantic import BaseModel


class PromptRequest(BaseModel):
    conversation_id: str
    prompt: str
    mode: str


class PromptResponse(BaseModel):
    reply: str