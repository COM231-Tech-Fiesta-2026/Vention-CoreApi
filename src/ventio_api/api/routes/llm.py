from fastapi import APIRouter, HTTPException, Depends
from src.ventio_api.services.llm_service import LLMService
from src.ventio_api.api.schema.llm_schema import PromptRequest, PromptResponse
from src.ventio_api.exceptions import (
    LLMAuthenticationException,
    LLMQuotaExhaustedException,
    LLMConnectionException
)


router = APIRouter(prefix="/llm", tags=["LLM"])


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
    except LLMAuthenticationException as e:
        raise HTTPException(status_code=401, detail=str(e))
    except LLMQuotaExhaustedException as e:
        raise HTTPException(status_code=429, detail=str(e))
    except LLMConnectionException as e:
        raise HTTPException(status_code=503, detail=str(e))