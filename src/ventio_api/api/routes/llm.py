from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from src.ventio_api.services.llm_service import LLMService


router = APIRouter(prefix="/llm", tags=["LLM"])


class PromptRequest(BaseModel):
    conversation_id: str
    prompt: str


class PromptResponse(BaseModel):
    reply: str


def get_llm_service():
    return LLMService()


@router.post("/ask", response_model=PromptResponse)
async def ask(
    data: PromptRequest,
    llm_service: LLMService = Depends(get_llm_service)
):
    try:
        reply = await llm_service.ask_llm(data.conversation_id, data.prompt)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))