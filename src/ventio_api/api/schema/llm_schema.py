from pydantic import BaseModel


class PromptRequest(BaseModel):
    conversation_id: str
    prompt: str
    mode: str


class PromptResponse(BaseModel):
    reply: str


class SummarizeResponse(BaseModel):
    title: str
    user_feelings: str
    description: str
