from fastapi import APIRouter, Depends
from ..schema.auth import AccessTokenContent
from ...services.summary_service import SummaryService
from ...infrastructure.auth.security import get_current_user_payload

router = APIRouter(prefix="/summaries")

summary = SummaryService()


@router.get("")
async def get_conversation_history(
    token: AccessTokenContent = Depends(get_current_user_payload),
):
    return await summary.get_history(token)
