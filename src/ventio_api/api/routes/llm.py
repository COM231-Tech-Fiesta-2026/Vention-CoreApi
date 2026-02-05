from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.ventio_api.services.llm_service import ask_llm


router = APIRouter(prefix="/llm", tags=["LLM"])


class PromptRequest(BaseModel):
    conversation_id: str
    prompt: str


class PromptResponse(BaseModel):
    reply: str


@router.post("/ask", response_model=PromptResponse)
async def ask(data: PromptRequest):
    try:
        reply = await ask_llm(data.conversation_id, data.prompt)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
