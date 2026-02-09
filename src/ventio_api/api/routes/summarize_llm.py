from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.ventio_api.services.llm_service import summarize, SummarizeResponse
from src.ventio_api.exceptions import (
    LLMAuthenticationException,
    LLMQuotaExhaustedException,
    LLMConnectionException
)


router = APIRouter(prefix="/llm", tags=["LLM"])


class SummarizeRequest(BaseModel):
    conversation_id: str
    conversation_text: str


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_endpoint(data: SummarizeRequest):
    try:
        result = await summarize(data.conversation_text)
        return result
    except LLMAuthenticationException as e:
        raise HTTPException(status_code=401, detail=str(e))
    except LLMQuotaExhaustedException as e:
        raise HTTPException(status_code=429, detail=str(e))
    except LLMConnectionException as e:
        raise HTTPException(status_code=503, detail=str(e))